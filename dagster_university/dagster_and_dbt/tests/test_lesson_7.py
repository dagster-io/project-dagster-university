from pathlib import Path

import dagster as dg
import pytest
import yaml

import src.dagster_and_dbt.completed.lesson_7.defs
from tests.fixtures import setup_dbt_env  # noqa: F401


@pytest.mark.parametrize("setup_dbt_env", ["lesson_7"], indirect=True)
def test_trips_partitioned_assets(setup_dbt_env):  # noqa: F811
    from src.dagster_and_dbt.completed.lesson_7.defs.assets import (
        metrics,
        requests,
        trips,
    )
    from src.dagster_and_dbt.completed.lesson_7.defs.resources import database_resource

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


@pytest.mark.parametrize("setup_dbt_env", ["lesson_7"], indirect=True)
def test_trips_by_week_partitioned_assets(setup_dbt_env):  # noqa: F811
    from src.dagster_and_dbt.completed.lesson_7.defs.assets import metrics
    from src.dagster_and_dbt.completed.lesson_7.defs.resources import database_resource

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


@pytest.mark.parametrize("setup_dbt_env", ["lesson_7"], indirect=True)
def test_dbt_partitioned_incremental_assets(setup_dbt_env):  # noqa: F811
    from src.dagster_and_dbt.completed.lesson_7.defs.assets import dbt
    from src.dagster_and_dbt.completed.lesson_7.defs.resources import dbt_resource

    dbt_analytics_assets = dg.load_assets_from_modules(modules=[dbt])

    result = dg.materialize(
        assets=[*dbt_analytics_assets],
        resources={
            "dbt": dbt_resource,
        },
        partition_key="2023-01-01",
    )
    assert result.success


@pytest.mark.parametrize("setup_dbt_env", ["lesson_7"], indirect=True)
def test_defs(setup_dbt_env):  # noqa: F811
    assert dg.Definitions.merge(
        dg.components.load_defs(src.dagster_and_dbt.completed.lesson_7.defs)
    )
