import dagster as dg

from ai_driven_data_engineering.completed.lesson_5.defs.assets.trending_events import (
    daily_partitions,
    trending_events,
)

raw_ingestion_job = dg.define_asset_job(
    name="raw_ingestion_job",
    selection=dg.AssetSelection.groups("raw")
    - dg.AssetSelection.assets(trending_events),
)

daily_raw_schedule = dg.ScheduleDefinition(
    name="daily_raw_8am_est",
    job=raw_ingestion_job,
    cron_schedule="0 8 * * *",
    execution_timezone="America/New_York",
    description="Materialize all raw assets every day at 8 AM Eastern.",
    default_status=dg.DefaultScheduleStatus.RUNNING,
)

trending_events_job = dg.define_asset_job(
    name="trending_events_job",
    selection=dg.AssetSelection.assets(trending_events),
    partitions_def=daily_partitions,
)

daily_trending_events_schedule = dg.build_schedule_from_partitioned_job(
    trending_events_job,
    name="daily_trending_events_8am_est",
    hour_of_day=8,
    minute_of_hour=0,
    default_status=dg.DefaultScheduleStatus.RUNNING,
    description="Fetch and append trending events daily at 8 AM Eastern.",
)
