from dagster import Definitions, load_assets_from_modules
from dagster_duckdb import DuckDBResource
import duckdb

from .assets import trips

all_assets = load_assets_from_modules([trips])

duckdb_resource = DuckDBResource(
    database="data.duckdb",
)

defs = Definitions(
    assets=all_assets,
    resources={
        "database": duckdb_resource
    }
)
