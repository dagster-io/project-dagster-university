import dagster as dg

import dagster_essentials.defs
from dagster_essentials.assets import metrics, trips

trip_assets = dg.load_assets_from_modules([trips])
metric_assets = dg.load_assets_from_modules([metrics])

defs = dg.Definitions.merge(
    dg.Definitions(assets=[*trip_assets, *metric_assets]),
    dg.components.load_defs(dagster_essentials.defs),
)
