import dagster as dg

from dagster_and_etl.completed.lesson_4.defs.jobs import (
    asteroid_job,
    asteroid_partition_job,
)


@dg.schedule(job=asteroid_job, cron_schedule="0 6 * * *")
def date_range_schedule(context):
    scheduled_date = context.scheduled_execution_time.strftime("%Y-%m-%d")

    return dg.RunRequest(
        run_config={
            "ops": {
                "asteroids": {
                    "config": {
                        "date": scheduled_date,
                    },
                },
            },
        },
    )


asset_partitioned_schedule = dg.build_schedule_from_partitioned_job(
    asteroid_partition_job,
)
