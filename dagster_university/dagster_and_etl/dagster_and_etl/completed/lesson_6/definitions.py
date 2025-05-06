import dagster as dg

import dagster_and_etl.completed.lesson_6.defs as defs

defs = dg.Definitions.merge(
    dg.components.load_defs(defs),
)
