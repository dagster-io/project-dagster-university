from dagster import Definitions, EnvVar, load_assets_from_modules
from dagster_duckdb import DuckDBResource
import duckdb

from .assets import trips, metrics
from .resources import duckdb_resource

trip_assets = load_assets_from_modules([trips])
metric_assets = load_assets_from_modules(
    modules=[metrics],
    group_name="metrics",
)

defs = Definitions(
    assets=[*trip_assets, *metric_assets],
    resources={
        "database": duckdb_resource
    }
)
