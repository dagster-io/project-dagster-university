import dagster as dg

import dagster_testing.defs


@dg.definitions
def defs():
    return dg.load_defs(defs_root=dagster_testing.defs)
