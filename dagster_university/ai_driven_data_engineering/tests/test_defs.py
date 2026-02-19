import dagster as dg
import pytest

from ai_driven_data_engineering.definitions import defs as defs_fn


def test_defs_load():
    """Definitions load from the defs folder."""
    defs = defs_fn()
    assert defs is not None
    assert isinstance(defs, dg.Definitions)


def test_defs_has_raw_assets(defs):
    """Definitions include raw group assets."""
    asset_specs = list(defs.get_all_asset_specs())
    asset_keys = [spec.key for spec in asset_specs]
    assert dg.AssetKey("raw_customers") in asset_keys
    assert dg.AssetKey("raw_orders") in asset_keys
    assert dg.AssetKey("raw_payments") in asset_keys


def test_defs_has_job(defs):
    """Definitions include the raw ingestion job."""
    job = defs.get_job_def("raw_ingestion_job")
    assert job is not None
    assert job.name == "raw_ingestion_job"


def test_defs_has_schedule(defs):
    """Definitions include the daily raw schedule."""
    schedule = defs.get_schedule_def("daily_raw_8am_est")
    assert schedule is not None
    assert schedule.name == "daily_raw_8am_est"
    assert schedule.cron_schedule == "0 8 * * *"
