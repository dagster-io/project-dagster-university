import dagster as dg
from dagster_dlt import DagsterDltResource

import dagster_and_etl.completed.lesson_5.assets as assets

defs = dg.Definitions(
    assets=[
        assets.quickstart_duckdb_assets,
    ],
    resources={
        "dlt": DagsterDltResource(),
    },
)
