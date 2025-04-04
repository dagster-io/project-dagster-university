import dagster as dg

import dagster_and_etl.completed.lesson_3.jobs as jobs

asset_partitioned_schedule = dg.build_schedule_from_partitioned_job(
    jobs.import_partition_job,
    hour_of_day=1,
    minute_of_hour=30,
)
