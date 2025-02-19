from datetime import datetime

import dagster as dg

import dagster_testing.lesson_5.jobs as jobs
from dagster_testing.lesson_5.assets import (
    my_partitioned_config,
)
from dagster_testing.lesson_5.definitions import defs


def test_my_partitioned_config():
    run_config = my_partitioned_config(datetime(2020, 1, 3), datetime(2020, 1, 4))
    assert run_config == {
        "ops": {"process_data_for_date": {"config": {"date": "2020-01-03"}}}
    }


def test_jobs():
    assert jobs.my_job
    assert jobs.my_job_configured


def test_def():
    assert defs

    assert defs.get_assets_def("combine_asset")
    assert defs.get_job_def("jobs_config")
    assert defs.get_schedule_def("my_schedule")
    assert defs.get_sensor_def("my_sensor")
