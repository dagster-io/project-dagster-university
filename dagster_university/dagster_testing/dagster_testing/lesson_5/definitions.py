import dagster as dg
from dagster_snowflake import SnowflakeResource

import dagster_testing.lesson_5.assets as assets

all_assets = dg.load_assets_from_modules([assets])


snowflake_resource = SnowflakeResource(
    account=dg.EnvVar("SNOWFLAKE_ACCOUNT"),
    user=dg.EnvVar("SNOWFLAKE_USERNAME"),
    password=dg.EnvVar("SNOWFLAKE_PASSWORD"),
    warehouse=dg.EnvVar("SNOWFLAKE_WAREHOUSE"),
)


defs = dg.Definitions(
    assets=all_assets,
    resources={
        "database": snowflake_resource,
    },
)
