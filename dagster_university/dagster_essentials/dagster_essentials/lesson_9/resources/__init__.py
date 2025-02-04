from dagster import EnvVar
from dagster_duckdb import DuckDBResource

database_resource = DuckDBResource(
    database=EnvVar("DUCKDB_DATABASE"),
)
