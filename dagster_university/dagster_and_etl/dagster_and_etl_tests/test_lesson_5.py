from unittest.mock import Mock, patch

import dagster as dg
import pytest
from dagster_dlt import DagsterDltResource

import dagster_and_etl.completed.lesson_5.defs.assets as assets
import dagster_and_etl.completed.lesson_5.dlt_nasa as dlt_nasa
import dagster_and_etl.completed.lesson_5.dlt_quick_start as dlt_quick_start
from dagster_and_etl.completed.lesson_5.definitions import defs


@pytest.fixture()
def nasa_config():
    return assets.NasaDate(
        date="2025-04-01",
    )


@pytest.fixture()
def asteroid_response():
    return {
        "near_earth_objects": {
            "2015-09-07": [
                {
                    "links": {
                        "self": "http://api.nasa.gov/neo/rest/v1/neo/2004034?api_key=XXX"
                    },
                    "id": "2004034",
                    "neo_reference_id": "2004034",
                    "name": "4034 Vishnu (1986 PA)",
                    "nasa_jpl_url": "https://ssd.jpl.nasa.gov/tools/sbdb_lookup.html#/?sstr=2004034",
                    "absolute_magnitude_h": 18.49,
                    "estimated_diameter": {
                        "kilometers": {
                            "estimated_diameter_min": 0.5327886649,
                            "estimated_diameter_max": 1.1913516723,
                        },
                        "meters": {
                            "estimated_diameter_min": 532.7886648737,
                            "estimated_diameter_max": 1191.3516722989,
                        },
                        "miles": {
                            "estimated_diameter_min": 0.3310594255,
                            "estimated_diameter_max": 0.74027138,
                        },
                        "feet": {
                            "estimated_diameter_min": 1747.9943632641,
                            "estimated_diameter_max": 3908.634220545,
                        },
                    },
                    "is_potentially_hazardous_asteroid": True,
                    "close_approach_data": [
                        {
                            "close_approach_date": "2025-04-01",
                            "close_approach_date_full": "2025-Apr-01 10:03",
                            "epoch_date_close_approach": 1743501780000,
                            "relative_velocity": {
                                "kilometers_per_second": "11.9802215702",
                                "kilometers_per_hour": "43128.797652765",
                                "miles_per_hour": "26798.5576304083",
                            },
                            "miss_distance": {
                                "astronomical": "0.1567576329",
                                "lunar": "60.9787191981",
                                "kilometers": "23450607.988081923",
                                "miles": "14571532.1128716174",
                            },
                            "orbiting_body": "Earth",
                        }
                    ],
                    "is_sentry_object": False,
                },
            ]
        }
    }


def test_dlt_quick_start():
    load_info = dlt_quick_start.pipeline.run(dlt_quick_start.simple_source())
    assert load_info is not None


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


def test_dlt_quick_start_assets():
    result = dg.materialize(
        assets=[
            assets.dlt_simple,
        ],
        resources={
            "dlt": DagsterDltResource(),
        },
    )
    assert result.success


def test_dlt_csv_assets():
    result = dg.materialize(
        assets=[
            assets.import_file,
            assets.dlt_load_csv,
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


def test_dlt_nasa_assets(nasa_config):
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


@patch("requests.get")
def test_dlt_nasa_assets_partition(mock_get, asteroid_response):
    mock_response = Mock()
    mock_response.json.return_value = asteroid_response
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = dg.materialize(
        assets=[
            assets.dlt_nasa_partition,
        ],
        resources={
            "dlt": DagsterDltResource(),
        },
        partition_key="2015-09-07",
    )
    assert result.success


def test_def_can_load():
    assert defs
