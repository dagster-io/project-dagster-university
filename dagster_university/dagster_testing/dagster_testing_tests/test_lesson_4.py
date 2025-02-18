from contextlib import contextmanager

import dagster as dg
import psycopg2
import pytest

from dagster_testing.lesson_4.assets import (
    my_sql_table,
)

from .fixtures import docker_compose  # noqa: F401


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
