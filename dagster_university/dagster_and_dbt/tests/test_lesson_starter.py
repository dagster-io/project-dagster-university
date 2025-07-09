import dagster as dg

import src.dagster_and_dbt.defs


def test_defs():
    assert dg.Definitions.merge(dg.components.load_defs(src.dagster_and_dbt.defs))
