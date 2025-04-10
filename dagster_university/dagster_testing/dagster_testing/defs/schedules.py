import dagster as dg

import dagster_testing.defs.jobs as jobs
from dagster_testing.defs.assets import lesson_6

my_schedule = dg.ScheduleDefinition(
    name="my_schedule",
    job=jobs.my_job,
    cron_schedule="0 0 5 * *",  # every 5th of the month at midnight
    run_config=dg.RunConfig(
        {
            "state_population_file_config": lesson_6.FilepathConfig(
                path="dagster_testing_tests/data/test.csv"
            )
        }
    ),
)
