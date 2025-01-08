from dagster import Definitions, load_assets_from_modules

from .assets import trips, metrics, requests, _trips
from .resources import database_resource
from .jobs import trip_update_job, weekly_update_job, adhoc_request_job
from .schedules import trip_update_schedule, weekly_update_schedule
from .sensors import adhoc_request_sensor

trip_assets = load_assets_from_modules([trips])
metric_assets = load_assets_from_modules(
    modules=[metrics],
    group_name="metrics",
)
requests_assets = load_assets_from_modules(
    modules=[requests],
    group_name="requests",
)

all_jobs = [trip_update_job, weekly_update_job, adhoc_request_job]
all_schedules = [trip_update_schedule, weekly_update_schedule]
all_sensors = [adhoc_request_sensor]

# Only use the definition that applies to the section you are running
# This is mostly when updating screenshots
defs = Definitions(
    assets=trip_assets + metric_assets + requests_assets,
    resources={
        "database": database_resource,
    },
    jobs=all_jobs,
    schedules=all_schedules,
    sensors=all_sensors,
    metadata={
        "lessons": ["1","2","5","7","8","9"]
    },
)

# defs = Definitions(
#     assets=[_trips.taxi_trips_file_lesson_3],
#     metadata={
#         "lessons": ["3"]
#     },
# )

# defs = Definitions(
#     assets=[trips.taxi_trips_file, trips.taxi_zones_file],
#     metadata={
#         "lessons": ["4a"]
#     },
# )

# defs = Definitions(
#     assets=[trips.taxi_trips_file, trips.taxi_zones_file, trips.taxi_trips],
#     metadata={
#         "lessons": ["4b"]
#     },
# )

# defs = Definitions(
#     assets=[trips.taxi_trips, trips.taxi_zones, metrics.trips_by_week, metrics.manhattan_stats],
#     resources={
#         "database": database_resource,
#     },
#     metadata={
#         "lessons": ["6"]
#     },
# )
