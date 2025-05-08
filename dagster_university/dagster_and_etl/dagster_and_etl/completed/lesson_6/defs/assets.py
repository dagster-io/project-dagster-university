import dagster as dg
import dlt
from dagster_dlt import DagsterDltResource, dlt_assets
from dlt.sources.sql_database import sql_database


@dlt_assets(
    dlt_source=sql_database(),
    dlt_pipeline=dlt.pipeline(
        pipeline_name="postgres_pipeline",
        destination="postgres",
        dataset_name="postgres_data",
    ),
)
def dlt_postgres_assets(context: dg.AssetExecutionContext, dlt: DagsterDltResource):
    yield from dlt.run(context=context, dlt_source=sql_database())
