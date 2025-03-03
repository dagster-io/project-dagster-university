import dagster as dg

import dagster_testing.lesson_6.assets as assets
import dagster_testing.lesson_6.jobs as jobs

my_schedule = dg.ScheduleDefinition(
    name="my_schedule",
    job=jobs.my_job,
    cron_schedule="0 0 5 * *",  # every 5th of the month at midnight
    run_config=dg.RunConfig(
        {
            "state_population_file_config": assets.FilepathConfig(
                path="dagster_testing_tests/data/test.csv"
            )
        }
    ),
)
