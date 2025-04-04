import dagster as dg
from dagster_dlt import DagsterDltResource, dlt_assets

from dagster_and_etl.completed.lesson_5.dlt_quick_start import pipeline, simple_source


@dlt_assets(
    dlt_source=simple_source(),
    dlt_pipeline=pipeline,
    name="quick_start",
    group_name="dlt",
)
def quickstart_duckdb_assets(
    context: dg.AssetExecutionContext, dlt: DagsterDltResource
):
    yield from dlt.run(context=context)
