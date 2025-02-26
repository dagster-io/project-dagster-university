from unittest.mock import Mock, patch

import dagster as dg
import pytest

import dagster_testing.lesson_4.assets as assets
from dagster_testing.lesson_4.definitions import defs

EXAMPLE_RESPONSE = {
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


@patch("requests.get")
def test_state_population_api(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = EXAMPLE_RESPONSE
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = assets.state_population_api()

    assert len(result) == 2
    assert result[0] == {
        "city": "New York",
        "population": 8804190,
    }
    mock_get.assert_called_once_with(assets.API_URL, params={"state": "ny"})


@patch("requests.get")
def test_state_population_api_resource_mock(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = EXAMPLE_RESPONSE
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = assets.state_population_api_resource(assets.StatePopulation())

    assert len(result) == 2
    assert result[0] == {
        "city": "New York",
        "population": 8804190,
    }
    mock_get.assert_called_once_with(assets.API_URL, params={"state": "ny"})


@patch("requests.get")
def test_state_population_api_assets(mock_get, api_output):
    mock_response = Mock()
    mock_response.json.return_value = EXAMPLE_RESPONSE
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = dg.materialize(
        assets=[
            assets.state_population_api_resource,
            assets.total_population_resource,
        ],
        resources={"state_population_resource": assets.StatePopulation()},
    )
    assert result.success

    assert result.output_for_node("state_population_api_resource") == api_output
    assert result.output_for_node("total_population_resource") == 9082539


@patch("requests.get")
def test_state_population_api_assets_config(mock_get, api_output):
    mock_response = Mock()
    mock_response.json.return_value = EXAMPLE_RESPONSE
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = dg.materialize(
        assets=[
            assets.state_population_api_resource_config,
            assets.total_population_resource_config,
        ],
        resources={"state_population_resource": assets.StatePopulation()},
        run_config=dg.RunConfig(
            {"state_population_api_resource_config": assets.StateConfig(name="ny")}
        ),
    )
    assert result.success

    assert result.output_for_node("state_population_api_resource_config") == api_output
    assert result.output_for_node("total_population_resource_config") == 9082539


def test_state_population_api_mocked_resource():
    fake_city = {
        "city": "Fakestown",
        "population": 42,
    }

    mocked_resource = Mock()
    mocked_resource.get_cities.return_value = [fake_city]

    result = assets.state_population_api_resource(mocked_resource)

    assert len(result) == 1
    assert result[0] == fake_city


def test_def():
    assert defs
