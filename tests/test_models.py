import pytest

from fractal_challenge.models import Survey, Observation


@pytest.fixture(scope='module')
def new_survey():
    survey = Survey(id=1, name='survey1')
    return survey


@pytest.fixture(scope='module')
def new_observation():
    survey = Survey(id=1, name='survey1')
    observation = Observation(id=4, survey_id=survey.id, value=2.1, frequency=3)
    survey.observations.append(observation)
    return observation


def test_new_survey(new_survey):
    assert new_survey.name == 'survey1'


def test_new_observation(new_observation):
    assert new_observation.value == 2.1
    assert new_observation.frequency == 3
    assert new_observation.survey.name == 'survey1'
