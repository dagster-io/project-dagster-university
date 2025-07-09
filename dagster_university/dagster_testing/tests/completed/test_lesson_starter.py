import dagster as dg

import dagster_testing.defs


def test_defs():
    assert dg.Definitions.merge(dg.components.load_defs(dagster_testing.defs))
