from contextlib import contextmanager

import dagster as dg
import psycopg2
import pytest
from dagster_snowflake import SnowflakeResource

from dagster_testing.defs.assets import lesson_5

from .fixtures import docker_compose  # noqa: F401


@pytest.fixture
def query_output_ny():
    return [
        ("New York", 8804190),
        ("Buffalo", 278349),
    ]


@pytest.fixture
def query_output_ca():
    return [
        ("Los Angeles", 3898747),
    ]


@pytest.fixture
def postgres_resource():
    return PostgresResource(
        host="localhost",
        user="test_user",
        password="test_pass",
        database="test_db",
    )


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

    lesson_5.state_population_database(snowflake_staging_resource)


def test_state_population_database():
    pass


def test_total_population_database():
    pass


def test_assets():
    pass
