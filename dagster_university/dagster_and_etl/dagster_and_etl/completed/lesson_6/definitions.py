import dagster as dg

import dagster_and_etl.completed.lesson_6.defs


@dg.definitions
def defs():
    return dg.load_defs(defs_root=dagster_and_etl.completed.lesson_6.defs)
