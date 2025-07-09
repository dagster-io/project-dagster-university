import dagster as dg

import dagster_essentials.completed.lesson_3.defs
from dagster_essentials.completed.lesson_3.defs.assets import trips


def test_assets():
    assets = [trips.taxi_trips_file, trips.taxi_zones_file]
    result = dg.materialize(assets)
    assert result.success


def test_defs():
    assert dg.Definitions.merge(
        dg.components.load_defs(dagster_essentials.completed.lesson_3.defs)
    )
