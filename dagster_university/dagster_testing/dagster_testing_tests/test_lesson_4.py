from contextlib import contextmanager

import dagster as dg
import psycopg2
import pytest
from dagster_snowflake import SnowflakeResource

from dagster_testing.lesson_4.assets import (
    my_sql_table,
)
from dagster_testing.lesson_4.definitions import defs

from .fixtures import docker_compose  # noqa: F401


# Snowflake not configured
@pytest.mark.skip
def test_snowflake_staging():
    snowflake_staging_resource = SnowflakeResource(
        account=dg.EnvVar("SNOWFLAKE_ACCOUNT"),
        user=dg.EnvVar("SNOWFLAKE_USERNAME"),
        password=dg.EnvVar("SNOWFLAKE_PASSWORD"),
        database="STAGING",
        warehouse="STAGING_WAREHOUSE",
    )

    my_sql_table(snowflake_staging_resource)


class PostgresResource(dg.ConfigurableResource):
    user: str
    password: str
    host: str
    database: str

    def _connection(self):
        return psycopg2.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            database=self.database,
        )

    @contextmanager
    def get_connection(self):
        yield self._connection()


@pytest.mark.integration
def test_my_sql_table(docker_compose):  # noqa: F811
    postgres_resource = PostgresResource(
        host="localhost", user="test_user", password="test_pass", database="test_db"
    )

    my_sql_table(postgres_resource)


@pytest.mark.integration
def test_def():
    assert defs
