from dagster import Definitions, EnvVar, load_assets_from_modules
from os import environ

from .assets import trips, metrics
from .resources import get_database_resource
from .sensors import make_slack_on_failure_sensor
from .schedules import monthly_raw_files_schedule

trip_assets = load_assets_from_modules([trips])
metric_assets = load_assets_from_modules(
    modules=[metrics],
    group_name="metrics",
)

all_sensors = [make_slack_on_failure_sensor(base_url="my_dagit_url")]
all_schedules = [monthly_raw_files_schedule]

environment = environ.get("DAGSTER_ENVIRONMENT", "local")
database_resource = get_database_resource(environment)

defs = Definitions(
    assets=[*trip_assets, *metric_assets],
    resources={
        "database": database_resource
    },
    # sensors=all_sensors,
    schedules=all_schedules
)
