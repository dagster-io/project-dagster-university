from dagster import Definitions, load_assets_from_modules
from dagster_duckdb import DuckDBResource
import duckdb

from . import assets

all_assets = load_assets_from_modules([assets])

duckdb_resource = DuckDBResource(
    database="data.duckdb",
)

defs = Definitions(
    assets=all_assets,
    resources={
        "database": duckdb_resource
    }
)
