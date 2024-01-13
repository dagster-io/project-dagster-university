from dagster import Definitions, load_assets_from_modules

from .assets import trips, metrics, requests, dbt
from .resources import database_resource, dbt_resource
from .jobs import trip_update_job, weekly_update_job, adhoc_request_job, full_refresh_dbt_job
from .schedules import trip_update_schedule, weekly_update_schedule
from .sensors import adhoc_request_sensor

## Lesson 5 -> prob every other section after that
trip_assets = load_assets_from_modules([trips])
metric_assets = load_assets_from_modules(
    modules=[metrics],
    group_name="metrics",
)
requests_assets = load_assets_from_modules(
    modules=[requests],
    group_name="requests",
)
dbt_analytics_assets = load_assets_from_modules(modules=[dbt])

all_jobs = [trip_update_job, weekly_update_job, adhoc_request_job, full_refresh_dbt_job]
all_schedules = [trip_update_schedule, weekly_update_schedule]
all_sensors = [adhoc_request_sensor]

defs = Definitions(
    assets=trip_assets + metric_assets + requests_assets + dbt_analytics_assets,
    resources={
        "database": database_resource,
        "dbt": dbt_resource,
    },
    jobs=all_jobs,
    schedules=all_schedules,
    sensors=all_sensors,
)
