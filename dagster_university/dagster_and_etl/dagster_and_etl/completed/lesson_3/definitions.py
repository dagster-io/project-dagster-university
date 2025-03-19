import dagster as dg
from dagster_duckdb import DuckDBResource

import dagster_and_etl.completed.lesson_3.assets as assets
import dagster_and_etl.completed.lesson_3.schedules as schedules
import dagster_and_etl.completed.lesson_3.sensors as sensors

all_assets = dg.load_assets_from_modules([assets])


defs = dg.Definitions(
    assets=all_assets,
    asset_checks=[assets.not_empty],
    schedules=[schedules.asset_partitioned_schedule],
    sensors=[sensors.dynamic_sensor],
    resources={
        "database": DuckDBResource(
            database="data/staging/data.duckdb",
        ),
    },
)
