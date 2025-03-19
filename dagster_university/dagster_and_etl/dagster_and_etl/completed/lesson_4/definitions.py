import dagster as dg
from dagster_duckdb import DuckDBResource

import dagster_and_etl.completed.lesson_4.assets as assets

all_assets = dg.load_assets_from_modules([assets])


defs = dg.Definitions(
    assets=all_assets,
    resources={
        "nasa": assets.NASAResource(
            api_key=dg.EnvVar("NASA_API_KEY"),
        ),
        "database": DuckDBResource(
            database="data/staging/data.duckdb",
        ),
    },
)
