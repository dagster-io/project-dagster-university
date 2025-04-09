import dagster as dg

import dagster_essentials.completed.lesson_9.defs as defs
from dagster_essentials.completed.lesson_9.defs.resources import database_resource

defs = dg.Definitions.merge(
    dg.Definitions(
        resources={
            "database": database_resource,
        },
    ),
    dg.components.load_defs(defs),
)
