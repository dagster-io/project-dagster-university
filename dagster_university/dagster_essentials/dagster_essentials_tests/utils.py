import os

import duckdb
from dagster._utils.backoff import backoff


def duckdb_query(query: str):
    conn = backoff(
        fn=duckdb.connect,
        retry_on=(RuntimeError, duckdb.IOException),
        kwargs={
            "database": os.getenv("DUCKDB_DATABASE"),
        },
        max_retries=10,
    )
    return conn.execute(query).fetchall()
