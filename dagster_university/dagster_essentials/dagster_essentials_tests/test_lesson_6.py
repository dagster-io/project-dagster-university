import dagster as dg

from dagster_essentials.lesson_6.assets import metrics, trips
from dagster_essentials.lesson_6.definitions import defs
from dagster_essentials.lesson_6.resources import database_resource


def test_assets():
    assets = [
        trips.taxi_trips_file,
        trips.taxi_zones_file,
        trips.taxi_trips,
        trips.taxi_zones,
        metrics.trips_by_week,
        metrics.manhattan_stats,
        metrics.manhattan_map,
    ]
    result = dg.materialize(
        assets=assets,
        resources={
            "database": database_resource,
        },
    )
    assert result.success


def test_def_can_load():
    assert defs
