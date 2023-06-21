from dagster_duckdb import DuckDBResource
from dagster_dbt.cli import DbtCli
from dagster import EnvVar, file_relative_path

## Lesson 6 and go over .env file 
database_resource = DuckDBResource(
    database=EnvVar("DUCKDB_DATABASE"),
)

project_dir = file_relative_path(__file__, "../../transformations")

dbt_resource = DbtCli(
    project_dir=project_dir
)