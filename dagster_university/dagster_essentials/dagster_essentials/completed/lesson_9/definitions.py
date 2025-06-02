import dagster as dg

import dagster_essentials.completed.lesson_9.defs


@dg.definitions
def defs():
    return dg.load_defs(defs_root=dagster_essentials.completed.lesson_9.defs)
