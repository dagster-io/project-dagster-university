import dagster as dg

from dagster_essentials.completed.lesson_4.assets import metrics, trips

trip_assets = dg.load_assets_from_modules([trips])
metric_assets = dg.load_assets_from_modules([metrics])


defs = dg.Definitions(
    assets=trip_assets + metric_assets,
)
