import dagster as dg

import dagster_testing.jobs as jobs
import dagster_testing.resources as resources
import dagster_testing.schedules as schedules
import dagster_testing.sensors as sensors
from dagster_testing.assets import lesson_3, lesson_4, lesson_5, lesson_6

lesson_3_assets = dg.load_assets_from_modules([lesson_3])
lesson_4_assets = dg.load_assets_from_modules([lesson_4])
lesson_5_assets = dg.load_assets_from_modules([lesson_5])
lesson_6_assets = dg.load_assets_from_modules([lesson_6])


defs = dg.Definitions(
    assets=lesson_3_assets + lesson_4_assets + lesson_5_assets + lesson_6_assets,
    asset_checks=[lesson_6.non_negative],
    jobs=[jobs.my_job, jobs.my_job_configured],
    resources={
        "state_population_resource": resources.StatePopulation(),
        "database": dg.ResourceDefinition.mock_resource(),
    },
    schedules=[schedules.my_schedule],
    sensors=[sensors.my_sensor],
)
