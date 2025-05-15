import dagster as dg

from dagster_and_etl.completed.lesson_5.defs.jobs import (
    dlt_nasa_partition_job,
)

asset_partitioned_schedule = dg.build_schedule_from_partitioned_job(
    dlt_nasa_partition_job,
)
