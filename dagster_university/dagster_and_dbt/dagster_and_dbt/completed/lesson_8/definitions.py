import dagster as dg
from dagster_components import load_defs

# Import extra credit
import dagster_and_dbt.completed.lesson_8.components.defs
from dagster_and_dbt.completed.lesson_8.assets import metrics, requests, trips

# from dagster_and_dbt.completed.lesson_8.jobs import adhoc_request_job, trip_update_job, weekly_update_job
from dagster_and_dbt.completed.lesson_8.jobs import adhoc_request_job, weekly_update_job
from dagster_and_dbt.completed.lesson_8.resources import database_resource

# from dagster_and_dbt.completed.lesson_8.schedules import trip_update_schedule, weekly_update_schedule
from dagster_and_dbt.completed.lesson_8.schedules import weekly_update_schedule
from dagster_and_dbt.completed.lesson_8.sensors import adhoc_request_sensor

trip_assets = dg.load_assets_from_modules([trips])
metric_assets = dg.load_assets_from_modules(
    modules=[metrics],
    group_name="metrics",
)
requests_assets = dg.load_assets_from_modules(
    modules=[requests],
    group_name="requests",
)

all_jobs = [weekly_update_job, adhoc_request_job]
all_schedules = [weekly_update_schedule]
all_sensors = [adhoc_request_sensor]


defs = dg.Definitions.merge(
    dg.Definitions(
        assets=[
            *trip_assets,
            *metric_assets,
            *requests_assets,
            # Remove in favor of components
            # *dbt_analytics_assets,
        ],
        resources={
            "database": database_resource,
            # Resource no longer necessary
            # "dbt": dbt_resource,
        },
        jobs=all_jobs,
        schedules=all_schedules,
        sensors=all_sensors,
    ),
    load_defs(dagster_and_dbt.completed.lesson_8.components.defs),
)
