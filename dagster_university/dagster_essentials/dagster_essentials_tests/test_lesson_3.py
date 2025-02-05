import dagster as dg
from dagster_essentials.lesson_3.assets import trips


def test_assets():
    assets = [trips.taxi_trips_file, trips.taxi_zones_file]
    result = dg.materialize(assets)
    assert result.success
