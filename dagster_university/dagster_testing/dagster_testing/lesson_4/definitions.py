import dagster as dg
from dagster_snowflake import SnowflakeResource

from .assets import my_sql_table

snowflake_resource = SnowflakeResource(
    account=dg.EnvVar("SNOWFLAKE_ACCOUNT"),
    user=dg.EnvVar("SNOWFLAKE_USERNAME"),
    password=dg.EnvVar("SNOWFLAKE_PASSWORD"),
    warehouse=dg.EnvVar("SNOWFLAKE_WAREHOUSE"),
)


defs = dg.Definitions(
    assets=[my_sql_table],
    resources={
        "database": snowflake_resource,
    },
)
