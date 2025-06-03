import dagster as dg

from dagster_testing.definitions import defs


def test_def_can_load():
    assert defs
