import dagster as dg

from dagster_and_etl.completed.lesson_6.defs.jobs import (
    orders_refresh_job,
    postgres_refresh_job,
)

postgres_refresh_schedule = dg.ScheduleDefinition(
    job=postgres_refresh_job,
    cron_schedule="0 6 * * *",
)

orders_refresh_schedule = dg.ScheduleDefinition(
    job=orders_refresh_job,
    cron_schedule="0 12,18 * * *",
)
