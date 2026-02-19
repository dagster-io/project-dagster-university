import dagster as dg
import pytest

from ai_driven_data_engineering.defs.schedules import daily_raw


def test_raw_ingestion_job_exists():
    """raw_ingestion_job is defined and selects the raw group."""
    assert daily_raw.raw_ingestion_job is not None
    assert daily_raw.raw_ingestion_job.name == "raw_ingestion_job"
    assert daily_raw.raw_ingestion_job.selection == dg.AssetSelection.groups("raw")


def test_daily_raw_schedule_exists():
    """daily_raw_8am_est schedule is defined with correct cron and job."""
    assert daily_raw.daily_raw_schedule is not None
    assert daily_raw.daily_raw_schedule.name == "daily_raw_8am_est"
    assert daily_raw.daily_raw_schedule.cron_schedule == "0 8 * * *"
    assert daily_raw.daily_raw_schedule.execution_timezone == "America/New_York"
    assert daily_raw.daily_raw_schedule.job == daily_raw.raw_ingestion_job
