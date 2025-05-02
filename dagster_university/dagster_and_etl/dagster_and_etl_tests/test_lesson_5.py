import dagster as dg
from dagster_dlt import DagsterDltResource

import dagster_and_etl.completed.lesson_5.defs.assets as assets
from dagster_and_etl.completed.lesson_5.definitions import defs


def test_simple_dlt_assets():
    result = dg.materialize(
        assets=[assets.quickstart_duckdb_assets],
        resources={
            "dlt": DagsterDltResource(),
        },
    )
    assert result.success


def test_def_can_load():
    assert defs
