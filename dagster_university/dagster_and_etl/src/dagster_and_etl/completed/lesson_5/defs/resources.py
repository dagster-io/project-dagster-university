import dagster as dg
from dagster_dlt import DagsterDltResource


@dg.definitions
def resources():
    return dg.Definitions(
        resources={
            "dlt": DagsterDltResource(),
        },
    )
