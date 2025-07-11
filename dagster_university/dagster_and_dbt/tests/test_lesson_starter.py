import dagster as dg

import dagster_and_dbt.defs


def test_defs():
    assert dg.Definitions.merge(dg.components.load_defs(dagster_and_dbt.defs))
