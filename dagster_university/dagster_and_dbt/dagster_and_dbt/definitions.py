import dagster as dg

import dagster_and_dbt.defs

defs = dg.components.load_defs(dagster_and_dbt.defs)
