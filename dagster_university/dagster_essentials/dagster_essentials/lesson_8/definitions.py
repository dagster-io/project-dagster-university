import dagster as dg

from .assets import metrics, trips
from .jobs import trip_update_job, weekly_update_job
from .resources import database_resource
from .schedules import trip_update_schedule, weekly_update_schedule

trip_assets = dg.load_assets_from_modules([trips])
metric_assets = dg.load_assets_from_modules(
    modules=[metrics],
)

all_jobs = [trip_update_job, weekly_update_job]
all_schedules = [trip_update_schedule, weekly_update_schedule]

defs = dg.Definitions(
    assets=trip_assets + metric_assets,
    resources={
        "database": database_resource,
    },
    jobs=all_jobs,
    schedules=all_schedules,
)
