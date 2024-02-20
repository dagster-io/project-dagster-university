from dagster_duckdb import DuckDBResource
from dagster_dbt import DbtCliResource
from dagster import EnvVar
import boto3
import os

from ..assets.constants import DBT_DIRECTORY


database_resource = DuckDBResource(
    database=EnvVar("DUCKDB_DATABASE"),
)

if os.getenv("DAGSTER_ENVIRONMENT") == "prod":
    session = boto3.Session()
    smart_open_config = {"client": session.client("s3")}
else:
    smart_open_config = {}

dbt_resource = DbtCliResource(
    project_dir=DBT_DIRECTORY,
    target=os.getenv("DAGSTER_ENVIRONMENT", "dev")
)