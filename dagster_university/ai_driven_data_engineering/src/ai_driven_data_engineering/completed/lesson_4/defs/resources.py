from pathlib import Path

import dagster as dg
from dagster_duckdb import DuckDBResource


@dg.definitions
def resources():
    db_path = Path(__file__).parents[5] / "data" / "jaffle_shop.duckdb"
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return dg.Definitions(
        resources={
            "duckdb": DuckDBResource(database=str(db_path)),
        }
    )
