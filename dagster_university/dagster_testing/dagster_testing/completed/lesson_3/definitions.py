import dagster as dg

import dagster_testing.completed.lesson_3.assets as assets

all_assets = dg.load_assets_from_modules([assets])


defs = dg.Definitions(
    assets=all_assets,
)
