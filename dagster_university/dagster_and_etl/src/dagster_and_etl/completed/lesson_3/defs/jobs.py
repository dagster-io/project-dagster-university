import dagster as dg

import dagster_and_etl.completed.lesson_3.defs.assets as assets

import_partition_job = dg.define_asset_job(
    name="import_partition_job",
    selection=[
        assets.import_partition_file,
        assets.duckdb_partition_table,
    ],
)

import_dynamic_partition_job = dg.define_asset_job(
    name="import_dynamic_partition_job",
    selection=[
        assets.import_dynamic_partition_file,
        assets.duckdb_dynamic_partition_table,
    ],
)
