import dagster as dg

import dagster_testing.starter.lesson_4.assets as assets

all_assets = dg.load_assets_from_modules([assets])


defs = dg.Definitions(
    assets=all_assets,
    resources={
        "state_population_resource": assets.StatePopulation(),
    },
)
