from pathlib import Path

import dagster as dg
import yaml

import dagster_testing.lesson_5.assets as assets
import dagster_testing.lesson_5.jobs as jobs

my_schedule = dg.ScheduleDefinition(
    name="my_schedule",
    job=jobs.my_job,
    cron_schedule="0 0 5 * *",  # every 5th of the month at midnight
    run_config=dg.RunConfig({"config_asset": assets.AssetConfig(number=20)}),
)
