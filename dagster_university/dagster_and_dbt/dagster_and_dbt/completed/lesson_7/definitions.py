import dagster as dg

from .assets import dbt, metrics, requests, trips

# from .jobs import adhoc_request_job, trip_update_job, weekly_update_job
from .jobs import adhoc_request_job, weekly_update_job
from .resources import database_resource, dbt_resource

# from .schedules import trip_update_schedule, weekly_update_schedule
from .schedules import weekly_update_schedule
from .sensors import adhoc_request_sensor

trip_assets = dg.load_assets_from_modules([trips])
metric_assets = dg.load_assets_from_modules(
    modules=[metrics],
    group_name="metrics",
)
requests_assets = dg.load_assets_from_modules(
    modules=[requests],
    group_name="requests",
)
dbt_analytics_assets = dg.load_assets_from_modules(modules=[dbt])

all_jobs = [weekly_update_job, adhoc_request_job]
all_schedules = [weekly_update_schedule]
all_sensors = [adhoc_request_sensor]

defs = dg.Definitions(
    assets=[*trip_assets, *metric_assets, *requests_assets, *dbt_analytics_assets],
    resources={
        "database": database_resource,
        "dbt": dbt_resource,
    },
    jobs=all_jobs,
    schedules=all_schedules,
    sensors=all_sensors,
)
