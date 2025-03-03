from contextlib import contextmanager

import dagster as dg
import psycopg2
import pytest
from dagster_snowflake import SnowflakeResource

import dagster_testing.lesson_5.assets as assets
from dagster_testing.lesson_5.definitions import defs

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

    assets.state_population_database(snowflake_staging_resource)


@pytest.mark.integration
def test_state_population_database(docker_compose, query_output_ny):  # noqa: F811
    postgres_resource = PostgresResource(
        host="localhost",
        user="test_user",
        password="test_pass",
        database="test_db",
    )

    result = assets.state_population_database(postgres_resource)
    assert result == query_output_ny


@pytest.mark.integration
def test_total_population_database():
    input = [("City 1", 100), ("City 2", 200)]
    assert assets.total_population_database(input) == 300


@pytest.mark.integration
def test_assets_partition(docker_compose, postgres_resource, query_output_ny):  # noqa: F811
    result = dg.materialize(
        assets=[
            assets.state_population_database,
            assets.total_population_database,
        ],
        resources={"database": postgres_resource},
    )
    assert result.success

    assert result.output_for_node("state_population_database") == query_output_ny
    assert result.output_for_node("total_population_database") == 9082539


@pytest.mark.integration
def test_state_population_database_config(
    docker_compose,  # noqa: F811
    postgres_resource,
    query_output_ca,
):
    config = assets.StateConfig(name="CA")
    result = assets.state_population_database_config(config, postgres_resource)
    assert result == query_output_ca


@pytest.mark.integration
def test_def():
    assert defs
