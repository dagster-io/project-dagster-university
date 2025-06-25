import dagster as dg

import src.dagster_and_etl.completed.lesson_3.defs.jobs as jobs

asset_partitioned_schedule = dg.build_schedule_from_partitioned_job(
    jobs.import_partition_job,
    cron_schedule="0 6 * * *",
)
