import dagster as dg

import src.dagster_essentials.completed.lesson_6.defs
from src.dagster_essentials.completed.lesson_6.defs.assets import metrics, trips
from src.dagster_essentials.completed.lesson_6.defs.resources import database_resource


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


def test_defs():
    assert dg.Definitions.merge(
        dg.components.load_defs(src.dagster_essentials.completed.lesson_6.defs)
    )
