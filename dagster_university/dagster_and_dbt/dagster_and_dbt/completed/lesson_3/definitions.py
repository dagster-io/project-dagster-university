import dagster as dg

import dagster_and_dbt.completed.lesson_3.defs

defs = dg.components.load_defs(dagster_and_dbt.completed.lesson_3.defs)
