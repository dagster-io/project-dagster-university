import dagster as dg

import dagster_and_etl.completed.lesson_4.assets as assets

asteroid_job = dg.define_asset_job(
    name="asteroid_job",
    selection=[
        assets.asteroids,
        assets.asteroids_file,
        assets.duckdb_table,
    ],
)
