from pathlib import Path

import dagster as dg
from dagster_aws.s3 import S3Resource
from dagster_duckdb import DuckDBResource
from eventregistry import EventRegistry


class NewsApiResource(dg.ConfigurableResource):
    api_key: str

    def get_client(self) -> EventRegistry:
        return EventRegistry(apiKey=self.api_key)


@dg.definitions
def resources():
    db_path = Path(__file__).parents[3] / "data" / "jaffle_shop.duckdb"
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return dg.Definitions(
        resources={
            "duckdb": DuckDBResource(database=str(db_path)),
            "s3": S3Resource(
                endpoint_url=dg.EnvVar("AWS_ENDPOINT_URL_S3"),
                aws_access_key_id=dg.EnvVar("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=dg.EnvVar("AWS_SECRET_ACCESS_KEY"),
                region_name="us-east-1",
                use_ssl=False,
            ),
            "newsapi": NewsApiResource(api_key=dg.EnvVar("NEWS_API_KEY")),
        }
    )
