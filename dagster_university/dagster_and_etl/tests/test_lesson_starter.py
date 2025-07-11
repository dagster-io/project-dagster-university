import dagster as dg

import dagster_and_etl.defs


def test_defs():
    assert dg.Definitions.merge(dg.components.load_defs(dagster_and_etl.defs))
