from dagster_duckdb import DuckDBResource
from dagster_gcp import BigQueryResource
from dagster import EnvVar

def get_database_resource(environment):

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