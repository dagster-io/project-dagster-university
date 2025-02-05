import os

import duckdb
import pytest
from dagster._utils.backoff import backoff


@pytest.fixture()
def drop_tax_trips_table():
    query = """
        drop table if exists trips;
    """

    conn = backoff(
        fn=duckdb.connect,
        retry_on=(RuntimeError, duckdb.IOException),
        kwargs={
            "database": os.getenv("DUCKDB_DATABASE"),
        },
        max_retries=10,
    )
    conn.execute(query)
