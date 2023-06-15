from dagster import AssetSelection, define_asset_job, ScheduleDefinition


raw_files_job = define_asset_job("raw_files_job", AssetSelection.groups('raw_files'))

monthly_raw_files_schedule = ScheduleDefinition(job=raw_files_job, cron_schedule="0 0 1 * *")