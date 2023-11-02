from dagster_duckdb import DuckDBResource
from dagster import EnvVar, file_relative_path
from dagster_dbt import DbtCliResource


## Lesson 6 and go over .env file 
database_resource = DuckDBResource(
    database=EnvVar("DUCKDB_DATABASE"),
)

dbt_resource = DbtCliResource(
    project_dir=file_relative_path(__file__, "../../dagster_university_dbt"),
    profiles_dir=file_relative_path(__file__, "../../dagster_university_dbt"),
    target='dev',
)
DBT_MANIFEST_PATH = file_relative_path(__file__, "../../dagster_university_dbt/target/manifest.json")
