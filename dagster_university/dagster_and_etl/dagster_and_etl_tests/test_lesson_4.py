from unittest.mock import Mock

import dagster as dg
import pytest
from dagster_duckdb import DuckDBResource

import dagster_and_etl.completed.lesson_4.defs as defs
import dagster_and_etl.completed.lesson_4.defs.assets as assets
from dagster_and_etl_tests.fixtures import nasa_response


@pytest.fixture()
def nasa_config():
    return assets.NasaDate(
        date="2025-04-01",
    )


@pytest.fixture()
def asteroid_response():
    return nasa_response


def test_asteroid_assets(nasa_config, asteroid_response):
    mocked_resource = Mock()
    mocked_resource.get_near_earth_asteroids.return_value = asteroid_response

    _assets = [
        assets.asteroids,
        assets.asteroids_file,
        assets.duckdb_table,
    ]
    result = dg.materialize(
        assets=_assets,
        resources={
            "nasa": mocked_resource,
            "database": DuckDBResource(
                database="data/staging/data.duckdb",
            ),
        },
        run_config=dg.RunConfig(
            {
                "asteroids": nasa_config,
            }
        ),
    )
    assert result.success

    mocked_resource.get_near_earth_asteroids.assert_called_once_with(
        start_date="2025-03-31",
        end_date="2025-04-01",
    )


def test_asteroid_partition_assets(asteroid_response):
    mocked_resource = Mock()
    mocked_resource.get_near_earth_asteroids.return_value = asteroid_response

    _assets = [
        assets.asteroids_partition,
    ]
    result = dg.materialize(
        assets=_assets,
        resources={"nasa": mocked_resource},
        partition_key="2025-04-01",
    )
    assert result.success

    mocked_resource.get_near_earth_asteroids.assert_called_once_with(
        start_date="2025-03-31",
        end_date="2025-04-01",
    )


def test_def_can_load():
    assert defs
