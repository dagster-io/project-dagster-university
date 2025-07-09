import dagster as dg

import src.dagster_testing.defs


def test_defs():
    assert dg.Definitions.merge(dg.components.load_defs(src.dagster_testing.defs))
