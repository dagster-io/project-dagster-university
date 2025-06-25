import os
from unittest.mock import Mock, patch

import dagster as dg
import pytest
from dagster_dlt import DagsterDltResource

import src.dagster_and_etl.completed.lesson_5.defs.assets as assets
import src.dagster_and_etl.completed.lesson_5.dlt_nasa as dlt_nasa
import src.dagster_and_etl.completed.lesson_5.dlt_quick_start as dlt_quick_start
from tests.nasa_data import nasa_response


@pytest.fixture()
def nasa_config():
    return assets.NasaDate(
        date="2015-09-07",
    )


@pytest.fixture()
def asteroid_response():
    return {"near_earth_objects": {"2015-09-07": nasa_response}}


# dlt pipelines
# def test_dlt_quick_start():
#     load_info = dlt_quick_start.pipeline.run(dlt_quick_start.simple_source())
#     assert load_info is not None


def test_simple_dlt_source():
    source = dlt_quick_start.simple_source()
    data = list(source.load_dict())

    assert len(data) == 2
    assert data[0] == {"id": 1, "name": "Alice"}
    assert data[1] == {"id": 2, "name": "Bob"}


@patch.dict(os.environ, {"NASA_API_KEY": "test_key", "DUCKDB_DATABASE": "test.db"})
def test_environment_variables():
    # Test that environment variables are properly used
    assert os.getenv("NASA_API_KEY") == "test_key"
    assert os.getenv("DUCKDB_DATABASE") == "test.db"


@patch("requests.get")
def test_dlt_nasa(mock_get, asteroid_response):
    mock_response = Mock()
    mock_response.json.return_value = asteroid_response
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    load_info = dlt_nasa.pipeline.run(
        dlt_nasa.nasa_neo_source(
            start_date="2015-09-07",
            end_date="2015-09-08",
            api_key="DEMO_KEY",
        )
    )
    assert load_info is not None

    mock_get.assert_called_once_with(
        "https://api.nasa.gov/neo/rest/v1/feed",
        params={
            "start_date": "2015-09-07",
            "end_date": "2015-09-08",
            "api_key": "DEMO_KEY",
        },
    )


# TODO: Enable multiple dlt assets
# dlt assets
# def test_dlt_quick_start_assets():
#     result = dg.materialize(
#         assets=[
#             assets.dlt_assets,
#         ],
#         resources={
#             "dlt": DagsterDltResource(),
#         },
#     )
#     assert result.success


def test_dlt_csv_assets():
    result = dg.materialize(
        assets=[
            assets.import_file,
            assets.dlt_csv_assets,
        ],
        resources={
            "dlt": DagsterDltResource(),
        },
        run_config=dg.RunConfig(
            {
                "import_file": assets.FilePath(path="2018-01-22.csv"),
            }
        ),
    )
    assert result.success


@patch("requests.get")
def test_dlt_nasa_assets(mock_get, nasa_config, asteroid_response):
    mock_response = Mock()
    mock_response.json.return_value = asteroid_response
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = dg.materialize(
        assets=[
            assets.dlt_nasa,
        ],
        resources={
            "dlt": DagsterDltResource(),
        },
        run_config=dg.RunConfig(
            {
                "dlt_nasa": nasa_config,
            }
        ),
    )
    assert result.success

    mock_get.assert_called_once_with(
        "https://api.nasa.gov/neo/rest/v1/feed",
        params={
            "start_date": "2015-09-06",
            "end_date": "2015-09-07",
            "api_key": "DEMO_KEY",
        },
    )


@patch("requests.get")
def test_dlt_nasa_assets_partition(mock_get, asteroid_response):
    mock_response = Mock()
    mock_response.json.return_value = asteroid_response
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = dg.materialize(
        assets=[
            assets.dlt_nasa_partition,
            assets.dlt_nasa_partition_eager,
        ],
        resources={
            "dlt": DagsterDltResource(),
        },
        partition_key="2015-09-07",
    )
    assert result.success

    mock_get.assert_called_once_with(
        "https://api.nasa.gov/neo/rest/v1/feed",
        params={
            "start_date": "2015-09-06",
            "end_date": "2015-09-07",
            "api_key": "DEMO_KEY",
        },
    )
