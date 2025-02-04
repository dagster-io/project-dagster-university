import dagster as dg
from dagster_and_dbt.lesson_7.assets import dbt, metrics, trips
from dagster_and_dbt.lesson_7.definitions import defs
from dagster_and_dbt.lesson_7.resources import database_resource, dbt_resource

dbt_analytics_assets = dg.load_assets_from_modules(modules=[dbt])


def test_trips_partitioned_assets():
    assets = [
        trips.taxi_trips_file,
        trips.taxi_zones_file,
        trips.taxi_trips,
        trips.taxi_zones,
        metrics.manhattan_stats,
        metrics.manhattan_map,
        metrics.airport_trips,
    ]
    result = dg.materialize(
        assets=assets,
        resources={
            "database": database_resource,
        },
        partition_key="2023-01-01",
    )
    assert result.success


def test_trips_by_week_partitioned_assets():
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


def test_dbt_partitioned_incremental_assets():
    result = dg.materialize(
        assets=[*dbt_analytics_assets],
        resources={
            "dbt": dbt_resource,
        },
        partition_key="2023-01-01",
    )
    assert result.success


def test_def_can_load():
    assert defs