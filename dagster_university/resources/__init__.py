from dagster_duckdb import DuckDBResource
from dagster_dbt.cli import DbtCli
from dagster import EnvVar, file_relative_path

from .postgres import PostgresResource

def get_database_resource(environment):

    print("Environment: ", environment)

    if environment == "prod":
        database_resource = PostgresResource(
            user=EnvVar("POSTGRES_USER"),
            password=EnvVar("POSTGRES_PASSWORD"),
            url=EnvVar("POSTGRES_URL"),
        )
    else:
        database_resource = DuckDBResource(
            database=EnvVar("DUCKDB_DATABASE"),
        )

    return database_resource

project_dir = file_relative_path(__file__, "../../transformations")

dbt_resource = DbtCli(
    project_dir=project_dir
)