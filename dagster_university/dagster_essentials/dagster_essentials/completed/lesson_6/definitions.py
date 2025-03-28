import dagster as dg

from dagster_essentials.completed.lesson_6.assets import metrics, trips
from dagster_essentials.completed.lesson_6.resources import database_resource

trip_assets = dg.load_assets_from_modules([trips])
metric_assets = dg.load_assets_from_modules([metrics])

defs = dg.Definitions(
    assets=trip_assets + metric_assets,
    resources={
        "database": database_resource,
    },
)
