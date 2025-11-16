# We'll generate a connection to DuckDb

import dagster as dg
from dagster_duckdb import DuckDBResource
from .assets import import_file, duckdb_table
from pathlib import Path

project_root = Path(__file__).resolve().parents[3]  # Adjust depending on depth
duckdb_path = project_root / "data/staging/data.duckdb"

defs = dg.Definitions(
    assets=[import_file, duckdb_table],
    resources={
        "database": DuckDBResource(
            # database=f"{duckdb_path}",
            database="data/staging/data.duckdb"
        )
    }
)
'''
@dg.definitions
def resources():
    return dg.Definitions(
        assets=[import_file, duckdb_table],
        resources={
            "database": DuckDBResource(
                database="data/staging/data.duckdb",
            )
        }
    )
'''    