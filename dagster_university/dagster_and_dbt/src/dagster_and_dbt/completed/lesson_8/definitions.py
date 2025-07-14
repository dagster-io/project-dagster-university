import dagster as dg

import dagster_and_dbt.completed.lesson_8.defs


@dg.definitions
def defs():
    return dg.load_defs(defs_root=dagster_and_dbt.completed.lesson_8.defs)
