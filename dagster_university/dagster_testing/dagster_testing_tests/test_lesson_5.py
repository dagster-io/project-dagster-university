from datetime import datetime

import dagster_testing.lesson_5.assets as assets
import dagster_testing.lesson_5.jobs as jobs
from dagster_testing.lesson_5.definitions import defs


def test_my_partitioned_config():
    run_config = assets.my_partitioned_config(
        datetime(2020, 1, 3), datetime(2020, 1, 4)
    )
    assert run_config == {
        "ops": {"process_data_for_date": {"config": {"date": "2020-01-03"}}}
    }


def test_non_negative():
    asset_check_pass = assets.non_negative(10)
    assert asset_check_pass.passed
    asset_check_fail = assets.non_negative(-10)
    assert not asset_check_fail.passed


def test_jobs():
    assert jobs.my_job
    assert jobs.my_job_configured


def test_def():
    assert defs

    assert defs.get_assets_def("combine_asset")
    assert defs.get_job_def("jobs_config")
    assert defs.get_schedule_def("my_schedule")
    assert defs.get_sensor_def("my_sensor")
