from dagster import materialize

from dagster_university.lesson_3.assets import trips


def test_assets():
    assets = [trips.taxi_trips_file, trips.taxi_zones_file]
    result = materialize(assets)
    assert result.success
