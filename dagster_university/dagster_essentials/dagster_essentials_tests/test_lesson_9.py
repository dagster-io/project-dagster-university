from pathlib import Path

import dagster as dg
import yaml

from dagster_essentials.completed.lesson_9.assets import metrics, requests, trips
from dagster_essentials.completed.lesson_9.definitions import defs
from dagster_essentials.completed.lesson_9.jobs import (
    adhoc_request_job,
    trip_update_job,
    weekly_update_job,
)
from dagster_essentials.completed.lesson_9.resources import database_resource
from dagster_essentials.completed.lesson_9.schedules import (
    trip_update_schedule,
    weekly_update_schedule,
)
from dagster_essentials.completed.lesson_9.sensors import (
    adhoc_request_sensor,
)
from dagster_essentials_tests.fixtures import drop_tax_trips_table  # noqa: F401


def test_trips_partitioned_assets(drop_tax_trips_table):  # noqa: F811
    assets = [
        trips.taxi_trips_file,
        trips.taxi_zones_file,
        trips.taxi_trips,
        trips.taxi_zones,
        metrics.manhattan_stats,
        metrics.manhattan_map,
        requests.adhoc_request,
    ]
    result = dg.materialize(
        assets=assets,
        resources={
            "database": database_resource,
        },
        partition_key="2023-01-01",
        run_config=yaml.safe_load(
            (Path(__file__).absolute().parent / "run_config.yaml").open()
        ),
    )
    assert result.success


def test_trips_by_week_partitioned_assets():
    assets = [
        metrics.trips_by_week,
    ]
    result = dg.materialize(
        assets=assets,
        resources={
            "database": database_resource,
        },
        partition_key="2023-01-01",
    )
    assert result.success


def test_jobs():
    assert trip_update_job
    assert weekly_update_job
    assert adhoc_request_job

    assert trip_update_job.name == "trip_update_job"
    assert weekly_update_job.name == "weekly_update_job"


def test_schedules():
    assert trip_update_schedule.cron_schedule == "0 0 5 * *"
    assert trip_update_schedule.job == trip_update_job
    assert weekly_update_schedule.cron_schedule == "0 0 * * 1"
    assert weekly_update_schedule.job == weekly_update_job


def test_sensors():
    assert adhoc_request_sensor


def test_def_can_load():
    assert defs
    assert defs.get_job_def("trip_update_job")
    assert defs.get_job_def("weekly_update_job")
    assert defs.get_schedule_def("trip_update_job_schedule")
    assert defs.get_schedule_def("weekly_update_job_schedule")
