import dagster as dg

from dagster_and_etl.definitions import defs


def test_def_can_load():
    assert defs
