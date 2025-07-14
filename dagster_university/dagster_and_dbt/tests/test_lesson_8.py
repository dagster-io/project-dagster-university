from pathlib import Path

import dagster as dg
import pytest
import yaml

import dagster_and_dbt.completed.lesson_8.defs
from dagster_and_dbt.completed.lesson_8.defs.assets import (
    metrics,
    requests,
    trips,
)
from dagster_and_dbt.completed.lesson_8.defs.resources import database_resource
from tests.fixtures import setup_dbt_env  # noqa: F401


@pytest.fixture()
def defs():
    return dg.Definitions.merge(
        dg.components.load_defs(dagster_and_dbt.completed.lesson_8.defs)
    )


@pytest.mark.parametrize("setup_dbt_env", ["lesson_8"], indirect=True)
def test_trips_partitioned_assets(setup_dbt_env, defs):  # noqa: F811
    assets = [
        trips.taxi_trips_file,
        trips.taxi_zones_file,
        trips.taxi_trips,
        trips.taxi_zones,
        metrics.manhattan_stats,
        metrics.manhattan_map,
        metrics.airport_trips,
        requests.adhoc_request,
    ]
    result = dg.materialize(
        assets=assets,
        resources={
            "database": database_resource,
        },
        partition_key="2023-01-01",
        run_config=yaml.safe_load(
            (Path(__file__).absolute().parent / "run_config.yaml").open()
        ),
    )
    assert result.success


@pytest.mark.parametrize("setup_dbt_env", ["lesson_8"], indirect=True)
def test_trips_by_week_partitioned_assets(setup_dbt_env):  # noqa: F811
    assets = [
        metrics.trips_by_week,
    ]
    result = dg.materialize(
        assets=assets,
        resources={
            "database": database_resource,
        },
        partition_key="2023-01-01",
    )
    assert result.success


@pytest.mark.parametrize("setup_dbt_env", ["lesson_8"], indirect=True)
def test_defs(setup_dbt_env, defs):  # noqa: F811
    assert defs
