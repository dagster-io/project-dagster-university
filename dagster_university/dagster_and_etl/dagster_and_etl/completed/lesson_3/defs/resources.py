import dagster as dg
from dagster_duckdb import DuckDBResource

defs = dg.Definitions(
    resources={
        "database": DuckDBResource(
            database="data/staging/data.duckdb",
        ),
    }
)
