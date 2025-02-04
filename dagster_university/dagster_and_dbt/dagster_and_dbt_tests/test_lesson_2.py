import dagster as dg
from dagster_and_dbt.lesson_2.assets import metrics, trips
from dagster_and_dbt.lesson_2.definitions import defs
from dagster_and_dbt.lesson_2.jobs import trip_update_job
from dagster_and_dbt.lesson_2.resources import database_resource


def test_trips_partitioned_assets():
    assets = [
        trips.taxi_trips_file,
        trips.taxi_zones_file,
        trips.taxi_trips,
        trips.taxi_zones,
        metrics.manhattan_stats,
        metrics.manhattan_map,
    ]
    result = dg.materialize(
        assets=assets,
        resources={
            "database": database_resource,
        },
        partition_key="2023-01-01",
    )
    assert result.success


def test_jobs():
    assert trip_update_job


def test_def_can_load():
    assert defs