import dagster as dg

raw_ingestion_job = dg.define_asset_job(
    name="raw_ingestion_job",
    selection=dg.AssetSelection.groups("raw"),
)

daily_raw_schedule = dg.ScheduleDefinition(
    name="daily_raw_8am_est",
    job=raw_ingestion_job,
    cron_schedule="0 8 * * *",
    execution_timezone="America/New_York",
    description="Materialize all raw assets every day at 8 AM Eastern.",
    default_status=dg.DefaultScheduleStatus.RUNNING,
)
