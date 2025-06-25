import dagster as dg
from dagster_duckdb import DuckDBResource


@dg.definitions
def resources():
    return dg.Definitions(
        resources={
            "database": DuckDBResource(
                database="data/staging/data.duckdb",
            ),
        }
    )
