import sys
import traceback

import numpy as np
from flask import json, Blueprint, request, render_template, Response

from .models import Survey, Observation


bp = Blueprint('my_app', __name__)


@bp.route('/', methods=['GET'])
def index():

    data = {
        'surveys': Survey.query.all(),
        'observations': Observation.query.all()
    }

    return render_template('index.html', data=data)


@bp.route('/survey/<int:survey_id>', methods=['GET', 'PUT', 'DELETE'])
@bp.route('/survey', methods=['GET', 'POST'])
def survey_all(survey_id=None):

    if request.method == 'PUT' and request.args.get('name') is None:
        return app_response("Insufficient params to update", 400)

    if request.method == "POST" and request.form.get('name') is None:
        return app_response("Insufficient params to add", 400)

    return app_response(data=Survey.get_delete_put_post(survey_id))


@bp.route('/stat/<int:observation_id>', methods=['GET', 'PUT', 'DELETE'])
@bp.route('/stat', methods=['GET'])
def observation_all(observation_id=None):

    if request.method == 'PUT' and request.args.get('value') is None and request.args.get('frequency') is None:
        return app_response("Insufficient params to update", 400)

    return app_response(data=Observation.get_delete_put_post(observation_id))


@bp.route('/stat/<int:survey_id>', methods=['POST'])
def observation_add(survey_id=None):

    if request.form.get('value') is None and request.form.get('frequency') is None:
        return app_response("Insufficient params to add", 400)

    try:
        survey = Survey.query.get_or_404(survey_id)
        return Observation.request_create_form(survey_id=survey.id).as_dict

    except Exception as ex:
        return app_response(str(ex), 400)


@bp.route('/results/<int:survey_id>', methods=['GET'])
def calculate_results(survey_id=None):

    try:
        if len(Observation.query.filter_by(survey_id=survey_id).all()) == 0:
            return app_response("No observations", 400)

        observations = Observation.query.filter_by(survey_id=survey_id).values('value', 'frequency')

        val, freq = np.array(list(observations)).T

        mean = np.average(val, weights=freq)

        ord = np.argsort(val)
        cdf = np.cumsum(freq[ord])

        if cdf[-1] % 2 == 0:
            st = cdf[-1] / 2.0
            end = st + 1

            a = val[ord][np.searchsorted(cdf, st)]
            b = val[ord][np.searchsorted(cdf, end)]
            median = (a + b) / 2.0

        else:
            median = val[ord][np.searchsorted(cdf, (cdf[-1] + 1) // 2.0)]

        mode = val[np.argmax(freq)]

        result = {
            "survey_id": survey_id,
            "observation_count": val.size,
            "mean": round(mean, 2),
            "mode": round(mode, 2),
            "median": round(median, 2)
        }

        return render_template('result.html', data=result)

    except Exception as ex:
        exception = "".join(traceback.format_exception(*sys.exc_info()))
        return app_response(exception, 400)


@bp.errorhandler(404)
def invalid_route(e):
    return app_response("Invalid route, object not found", 400)


def app_response(message=None, status=None, data=None):

    if isinstance(data, Response):
        status = data.status_code
        data = data.get_json()

    elif isinstance(data, tuple):
        status = data[1]
        message = data[0]
        data = None

    data = {
        'data': data,
        'error_message': message
    }

    return data, status
