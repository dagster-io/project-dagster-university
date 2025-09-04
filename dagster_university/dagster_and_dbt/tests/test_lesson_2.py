import dagster as dg
import pytest

import dagster_and_dbt.completed.lesson_2.defs
from dagster_and_dbt.completed.lesson_2.defs.resources import database_resource


@pytest.fixture()
def defs():
    return dg.components.load_defs(dagster_and_dbt.completed.lesson_2.defs)


def test_trips_partitioned_assets(defs):
    assets = [
        defs.get_assets_def(dg.AssetKey(["taxi_trips_file"])),
        defs.get_assets_def(dg.AssetKey(["taxi_zones_file"])),
        defs.get_assets_def(dg.AssetKey(["taxi_trips"])),
        defs.get_assets_def(dg.AssetKey(["taxi_zones"])),
        defs.get_assets_def(dg.AssetKey(["manhattan", "manhattan_stats"])),
        defs.get_assets_def(dg.AssetKey(["manhattan_map"])),
    ]
    result = dg.materialize(
        assets=assets,
        resources={
            "database": database_resource,
        },
        partition_key="2023-01-01",
    )
    assert result.success


def test_jobs(defs):
    assert defs.get_job_def("weekly_update_job")
    assert defs.get_job_def("adhoc_request_job")


def test_schedules(defs):
    assert defs.get_schedule_def("trip_update_job_schedule")
    assert defs.get_schedule_def("weekly_update_job_schedule")


def test_sensors(defs):
    assert defs.get_sensor_def("adhoc_request_sensor")


def test_defs(defs):
    assert defs
