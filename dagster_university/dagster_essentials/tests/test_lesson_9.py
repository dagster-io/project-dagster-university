from pathlib import Path

import dagster as dg
import pytest
import yaml

import dagster_essentials.completed.lesson_9.defs
from dagster_essentials.completed.lesson_9.defs.resources import database_resource
from tests.fixtures import drop_tax_trips_table  # noqa: F401


@pytest.fixture()
def defs():
    return dg.components.load_defs(dagster_essentials.completed.lesson_9.defs)


def test_trips_partitioned_assets(drop_tax_trips_table, defs):  # noqa: F811
    assets = [
        defs.get_assets_def(dg.AssetKey(["taxi_trips_file"])),
        defs.get_assets_def(dg.AssetKey(["taxi_zones_file"])),
        defs.get_assets_def(dg.AssetKey(["taxi_trips"])),
        defs.get_assets_def(dg.AssetKey(["taxi_zones"])),
        defs.get_assets_def(dg.AssetKey(["manhattan", "manhattan_stats"])),
        defs.get_assets_def(dg.AssetKey(["manhattan_map"])),
        defs.get_assets_def(dg.AssetKey(["adhoc_request"])),
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


def test_trips_by_week_partitioned_assets(defs):
    assets = [
        defs.get_assets_def(dg.AssetKey(["trips_by_week"])),
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
    assert defs.get_job_def("trip_update_job")
    assert defs.get_job_def("weekly_update_job")
    assert defs.get_job_def("adhoc_request_job")


def test_schedules(defs):
    assert defs.get_schedule_def("trip_update_job_schedule")
    assert defs.get_schedule_def("weekly_update_job_schedule")


def test_sensors(defs):
    assert defs.get_sensor_def("adhoc_request_sensor")


def test_defs(defs):
    assert defs
