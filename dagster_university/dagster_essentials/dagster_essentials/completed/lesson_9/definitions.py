import dagster as dg

import dagster_essentials.completed.lesson_9.defs as defs

defs = dg.Definitions.merge(
    dg.components.load_defs(defs),
)
