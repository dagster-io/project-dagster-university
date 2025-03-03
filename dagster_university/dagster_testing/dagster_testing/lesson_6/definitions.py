import dagster as dg

import dagster_testing.lesson_6.assets as assets
import dagster_testing.lesson_6.jobs as jobs
import dagster_testing.lesson_6.resources as resources
import dagster_testing.lesson_6.schedules as schedules
import dagster_testing.lesson_6.sensors as sensors

all_assets = dg.load_assets_from_modules([assets])

defs = dg.Definitions(
    assets=all_assets,
    asset_checks=[assets.non_negative],
    jobs=[jobs.my_job, jobs.my_job_configured],
    resources={
        "state_population_resource": resources.StatePopulation(),
    },
    schedules=[schedules.my_schedule],
    sensors=[sensors.my_sensor],
)
