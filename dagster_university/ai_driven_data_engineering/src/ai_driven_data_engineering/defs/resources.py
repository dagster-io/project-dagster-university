from pathlib import Path

import dagster as dg
from dagster_aws.s3 import S3Resource
from dagster_duckdb import DuckDBResource

_DB_PATH = Path(__file__).parents[3] / "data" / "jaffle_shop.duckdb"


@dg.definitions
def resources():
    _DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return dg.Definitions(
        resources={
            "duckdb": DuckDBResource(database=str(_DB_PATH)),
            "s3": S3Resource(
                endpoint_url=dg.EnvVar("AWS_ENDPOINT_URL_S3"),
                aws_access_key_id=dg.EnvVar("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=dg.EnvVar("AWS_SECRET_ACCESS_KEY"),
                region_name="us-east-1",
                use_ssl=False,
            ),
        }
    )
