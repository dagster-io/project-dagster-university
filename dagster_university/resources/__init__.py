from dagster_duckdb import DuckDBResource
from dagster import EnvVar



duckdb_resource = DuckDBResource(
    database=EnvVar("DUCKDB_DATABASE"),
)
