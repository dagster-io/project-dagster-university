import dagster as dg

import dagster_testing.lesson_5.assets as assets
import dagster_testing.lesson_5.jobs as jobs
import dagster_testing.lesson_5.resources as resources
import dagster_testing.lesson_5.schedules as schedules
import dagster_testing.lesson_5.sensors as sensors

all_assets = dg.load_assets_from_modules([assets])

defs = dg.Definitions(
    assets=all_assets,
    asset_checks=[assets.non_negative],
    jobs=[jobs.my_job, jobs.my_job_configured],
    resources={
        "number": resources.ExampleResource(api_key="ABC123"),
    },
    schedules=[schedules.my_schedule],
    sensors=[sensors.my_sensor],
)
