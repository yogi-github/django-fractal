import pytest

from fractal_challenge.app import db, create_app
from fractal_challenge.config import Config
from fractal_challenge.models import Survey, Observation


class TestConfig(Config):

    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'


@pytest.fixture
def client():

    flask_app = create_app(config_class=TestConfig)

    with flask_app.test_client() as client:
        with flask_app.app_context():
            db.create_all()

            s1 = Survey(id=1, name='survey1')
            s1.observations.append(Observation(id=1, survey_id=1, value=5.2, frequency=2))
            s1.observations.append(Observation(id=2, survey_id=1, value=10.3, frequency=4))
            s1.observations.append(Observation(id=3, survey_id=1, value=15.6, frequency=3))
            s1.observations.append(Observation(id=4, survey_id=1, value=25.1, frequency=1))

            s2 = Survey(id=2, name="survey2")
            objects = [
                s1,
                s2
            ]

            db.session.add_all(objects)

            db.session.commit()

            yield client

            db.drop_all()


def test_index(client):

    response = client.get('/')
    assert response.status_code == 200


def test_get_all_surveys(client):

    response = client.get('/survey')
    assert response.status_code == 200

    json_data = response.get_json()['data']
    assert len(json_data) == 2
    assert json_data[0]['name'] == 'survey1'
    assert json_data[1]['name'] == 'survey2'


def test_get_single_survey(client):

    response = client.get('/survey/1')
    assert response.status_code == 200

    json_data = response.get_json()['data']
    assert json_data['name'] == 'survey1'


def test_get_single_survey_invalid_id(client):

    response = client.get('/survey/3')
    assert response.status_code == 400


def test_create_an_survey(client):

    response = client.post('/survey', data={'name': 'create_survey'})
    assert response.status_code == 200

    json_data = response.get_json()['data']
    assert json_data['name'] == 'create_survey'


def test_create_an_survey_unique_name_error(client):

    response = client.post('/survey', data={'name': 'survey1'})
    assert response.status_code == 400


def test_create_an_survey_invalid_form_data(client):

    response = client.post('/survey', data={'names': 'create_survey'})
    assert response.status_code == 400


def test_update_survey(client):

    response = client.put('/survey/1?name=new_name')
    assert response.status_code == 200

    data = Survey.query.get(1)
    assert data.name == 'new_name'


def test_update_survey_no_query_params(client):

    response = client.put('/survey/1')
    assert response.status_code == 400


def test_update_survey_invalid_query_params(client):

    response = client.put('/survey/1?names=victoria')
    assert response.status_code == 400


def test_delete_survey(client):

    response = client.delete('/survey/2')
    assert response.status_code == 200


def test_delete_survey_referred_by_observation(client):

    response = client.delete('/survey/1')
    assert response.status_code == 200

    response = client.get('/survey/1')
    assert response.status_code == 400


def test_get_all_observations(client):

    response = client.get('/stat')
    assert response.status_code == 200

    json_data = response.get_json()['data']
    assert len(json_data) == 4


def test_get_an_observation(client):

    response = client.get('/stat/1')
    assert response.status_code == 200

    json_data = response.get_json()['data']
    assert json_data['value'] == 5.2
    assert json_data['frequency'] == 2


def test_get_an_observation_invalid_id(client):

    response = client.get('/stat/6')
    assert response.status_code == 400


def test_create_an_observation(client):

    response = client.post('/stat/1', data={'value': 5.5, 'frequency': 6})
    assert response.status_code == 200

    json_data = response.get_json()
    assert json_data['value'] == 5.5
    assert json_data['frequency'] == 6


def test_create_an_observation_invalid_form_data(client):

    response = client.post('/stat/1', data={'values': 5.5, 'frequency': 6})
    assert response.status_code == 400


def test_update_observation(client):

    response = client.put('/stat/1?value=3.3&frequency=3')
    assert response.status_code == 200

    data = Observation.query.get(1)
    assert data.value == 3.3
    assert data.frequency == 3


def test_update_observation_invalid_query_params(client):

    response = client.put('/stat/1?values=3.3&frequencies=3')
    assert response.status_code == 400


def test_update_observation_no_query_params(client):

    response = client.put('/stat/1')
    assert response.status_code == 400


def test_delete_observation(client):

    response = client.delete('/stat/4')
    assert response.status_code == 200


def test_delete_observation_invalid_id(client):

    response = client.delete('/stat/100')
    assert response.status_code == 400


def test_calculate_results(client):

    response = client.get('/results/1')
    assert response.status_code == 200


def test_calculate_results_no_observations_exists(client):

    response = client.get('/results/2')
    assert response.status_code == 400
