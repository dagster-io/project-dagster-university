import dagster as dg
import pytest

from ai_driven_data_engineering.defs.schedules import daily_raw


def test_raw_ingestion_job_exists():
    """raw_ingestion_job is defined."""
    assert daily_raw.raw_ingestion_job is not None
    assert daily_raw.raw_ingestion_job.name == "raw_ingestion_job"


def test_daily_raw_schedule_exists():
    """daily_raw_8am_est schedule is defined with correct cron and job."""
    assert daily_raw.daily_raw_schedule is not None
    assert daily_raw.daily_raw_schedule.name == "daily_raw_8am_est"
    assert daily_raw.daily_raw_schedule.cron_schedule == "0 8 * * *"
    assert daily_raw.daily_raw_schedule.execution_timezone == "America/New_York"
    assert daily_raw.daily_raw_schedule.job == daily_raw.raw_ingestion_job


def test_trending_events_job_exists():
    """trending_events_job is defined and uses the daily partition definition."""
    assert daily_raw.trending_events_job is not None
    assert daily_raw.trending_events_job.name == "trending_events_job"


def test_daily_trending_events_schedule_exists():
    """daily_trending_events_8am_est schedule is defined with correct cron and job."""
    assert daily_raw.daily_trending_events_schedule is not None
    assert (
        daily_raw.daily_trending_events_schedule.name == "daily_trending_events_8am_est"
    )
    assert daily_raw.daily_trending_events_schedule.cron_schedule == "0 8 * * *"
