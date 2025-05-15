import dagster as dg

import dagster_and_etl.completed.lesson_5.defs.assets as assets

dlt_nasa_partition_job = dg.define_asset_job(
    name="dlt_nasa_partition_job",
    selection=[
        assets.dlt_nasa_partition,
    ],
)
