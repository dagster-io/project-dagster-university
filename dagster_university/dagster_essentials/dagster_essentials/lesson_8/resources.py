import dagster as dg
from dagster_duckdb import DuckDBResource

database_resource = DuckDBResource(
    database=dg.EnvVar("DUCKDB_DATABASE"),
)
