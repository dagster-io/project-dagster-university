from dagster_duckdb import DuckDBResource
from dagster_gcp import BigQueryResource
from dagster import EnvVar

from os import environ

def get_database_resource():
    environment = environ.get("DAGSTER_ENVIRONMENT", "local")

    if environment == "prod":
        database_resource = BigQueryResource(
            gcp_credentials=EnvVar("GCP_CREDENTIALS"),
            location=EnvVar("GCP_LOCATION"),
            project=EnvVar("GCP_PROJECT"),
        )
    else:
        database_resource = DuckDBResource(
            database=EnvVar("DUCKDB_DATABASE"),
        )

    return database_resource