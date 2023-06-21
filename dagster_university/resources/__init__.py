from dagster_duckdb import DuckDBResource
from dagster import EnvVar

## Lesson 6 and go over .env file 
database_resource = DuckDBResource(
    database=EnvVar("DUCKDB_DATABASE"),
)