import dagster as dg

import src.dagster_and_dbt.completed.lesson_2.defs
from src.dagster_and_dbt.completed.lesson_2.defs.assets import metrics, trips
from src.dagster_and_dbt.completed.lesson_2.defs.jobs import trip_update_job
from src.dagster_and_dbt.completed.lesson_2.defs.resources import database_resource


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


def test_defs():
    assert dg.Definitions.merge(
        dg.components.load_defs(src.dagster_and_dbt.completed.lesson_2.defs)
    )
