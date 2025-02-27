import dagster as dg

from .assets import trips

trip_assets = dg.load_assets_from_modules([trips])

defs = dg.Definitions(
    assets=trip_assets,
)
