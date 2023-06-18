from dagster import ConfigurableResource
from dagster._utils.backoff import backoff
from contextlib import contextmanager
from pydantic import Field
from sqlalchemy import create_engine

class PostgresResource(ConfigurableResource):
    """Resource for interacting with a Postgres database.

    Examples:
        .. code-block:: python

            from dagster import Definitions, asset
            from dagster_postgres import PostgresResource

            @asset
            def my_table(postgres: PostgresResource):
                with postgres.get_connection() as conn:
                    conn.execute("SELECT * from MY_SCHEMA.MY_TABLE")

            defs = Definitions(
                assets=[my_table],
                resources={"postgres": PostgresResource(database="path/to/db.postgres")}
            )

    """

    user: str = Field()
    password: str = Field()
    url: str = Field()

    @contextmanager
    def get_connection(self):

        db_url = f"postgresql://{self.user}:{self.password}.{self.url}"

        conn = backoff(
            fn=create_engine,
            retry_on=(RuntimeError, ),
            kwargs={"url": db_url},
            max_retries=10,
        ).connect()

        yield conn

        conn.close()
