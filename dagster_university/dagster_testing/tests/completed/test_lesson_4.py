from unittest.mock import Mock, patch

import dagster as dg
import pytest

from src.dagster_testing.defs.assets import lesson_4


@pytest.fixture
def example_response():
    return {
        "cities": [
            {
                "city_name": "New York",
                "city_population": 8804190,
            },
            {
                "city_name": "Buffalo",
                "city_population": 278349,
            },
        ],
    }


@pytest.fixture
def api_output():
    return [
        {
            "city": "New York",
            "population": 8804190,
        },
        {
            "city": "Buffalo",
            "population": 278349,
        },
    ]


@pytest.fixture
def fake_city():
    return {
        "city": "Fakestown",
        "population": 42,
    }


@patch("requests.get")
def test_state_population_api(mock_get, example_response):
    mock_response = Mock()
    mock_response.json.return_value = example_response
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = lesson_4.state_population_api()

    assert len(result) == 2
    assert result[0] == {
        "city": "New York",
        "population": 8804190,
    }
    mock_get.assert_called_once_with(lesson_4.API_URL, params={"state": "ny"})


@patch("requests.get")
def test_state_population_api_resource_mock(mock_get, example_response):
    mock_response = Mock()
    mock_response.json.return_value = example_response
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = lesson_4.state_population_api_resource(lesson_4.StatePopulation())

    assert len(result) == 2
    assert result[0] == {
        "city": "New York",
        "population": 8804190,
    }
    mock_get.assert_called_once_with(lesson_4.API_URL, params={"state": "ny"})


@patch("requests.get")
def test_state_population_api_assets(mock_get, example_response, api_output):
    mock_response = Mock()
    mock_response.json.return_value = example_response
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = dg.materialize(
        assets=[
            lesson_4.state_population_api_resource,
            lesson_4.total_population_resource,
        ],
        resources={"state_population_resource": lesson_4.StatePopulation()},
    )
    assert result.success

    assert result.output_for_node("state_population_api_resource") == api_output
    assert result.output_for_node("total_population_resource") == 9082539


@patch("requests.get")
def test_state_population_api_assets_config(mock_get, example_response, api_output):
    mock_response = Mock()
    mock_response.json.return_value = example_response
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = dg.materialize(
        assets=[
            lesson_4.state_population_api_resource_config,
            lesson_4.total_population_resource_config,
        ],
        resources={"state_population_resource": lesson_4.StatePopulation()},
        run_config=dg.RunConfig(
            {"state_population_api_resource_config": lesson_4.StateConfig(name="ny")}
        ),
    )
    assert result.success

    assert result.output_for_node("state_population_api_resource_config") == api_output
    assert result.output_for_node("total_population_resource_config") == 9082539


def test_state_population_api_mocked_resource(fake_city):
    mocked_resource = Mock()
    mocked_resource.get_cities.return_value = [fake_city]

    result = lesson_4.state_population_api_resource(mocked_resource)

    assert len(result) == 1
    assert result[0] == fake_city


def test_state_population_api_assets_mocked_resource(fake_city):
    mocked_resource = Mock()
    mocked_resource.get_cities.return_value = [fake_city]

    result = dg.materialize(
        assets=[
            lesson_4.state_population_api_resource_config,
            lesson_4.total_population_resource_config,
        ],
        resources={"state_population_resource": mocked_resource},
        run_config=dg.RunConfig(
            {"state_population_api_resource_config": lesson_4.StateConfig(name="ny")}
        ),
    )
    assert result.success

    assert result.output_for_node("state_population_api_resource_config") == [fake_city]
    assert result.output_for_node("total_population_resource_config") == 42
