from dagster_duckdb import DuckDBResource
from dagster import EnvVar

## Lesson 6 and go over .env file 
database_resource = DuckDBResource(
    database=EnvVar("DUCKDB_DATABASE"),
)

from dagster_dbt import DbtCliResource
from dagster import EnvVar, file_relative_path

dbt_resource = DbtCliResource(
    project_dir=file_relative_path(__file__, "../../transformations"),
    profiles_dir=file_relative_path(__file__, "../../transformations"),
)
DBT_MANIFEST_PATH = file_relative_path(__file__, "../../transformations/target/manifest.json")
