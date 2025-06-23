import dagster as dg

import src.dagster_and_dbt.completed.lesson_4.defs


@dg.definitions
def defs():
    return dg.load_defs(defs_root=src.dagster_and_dbt.completed.lesson_4.defs)
