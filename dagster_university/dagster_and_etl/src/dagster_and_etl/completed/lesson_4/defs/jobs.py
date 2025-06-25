import dagster as dg

import src.dagster_and_etl.completed.lesson_4.defs.assets as assets

asteroid_job = dg.define_asset_job(
    name="asteroid_job",
    selection=[
        assets.asteroids,
        assets.asteroids_file,
        assets.duckdb_table,
    ],
)

asteroid_partition_job = dg.define_asset_job(
    name="asteroid_partition_job",
    selection=[
        assets.asteroids_partition,
    ],
)
