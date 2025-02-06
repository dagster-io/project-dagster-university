from pathlib import Path

import dagster as dg
import pytest
import yaml

from dagster_and_dbt_tests.fixtures import setup_dbt_env  # noqa: F401


@pytest.mark.parametrize("setup_dbt_env", ["lesson_7"], indirect=True)
def test_trips_partitioned_assets(setup_dbt_env): # noqa: F811
    from dagster_and_dbt.lesson_7.assets import metrics, requests, trips
    from dagster_and_dbt.lesson_7.resources import database_resource

    assets = [
        trips.taxi_trips_file,
        trips.taxi_zones_file,
        trips.taxi_trips,
        trips.taxi_zones,
        metrics.manhattan_stats,
        metrics.manhattan_map,
        metrics.airport_trips,
        requests.adhoc_request
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
def test_trips_by_week_partitioned_assets(setup_dbt_env): # noqa: F811
    from dagster_and_dbt.lesson_7.assets import metrics
    from dagster_and_dbt.lesson_7.resources import database_resource

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
def test_dbt_partitioned_incremental_assets(setup_dbt_env): # noqa: F811
    from dagster_and_dbt.lesson_7.assets import dbt
    from dagster_and_dbt.lesson_7.resources import dbt_resource

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
def test_def_can_load(setup_dbt_env): # noqa: F811
    from dagster_and_dbt.lesson_7.definitions import defs

    assert defs