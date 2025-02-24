from unittest.mock import patch

import dagster as dg

import dagster_testing.lesson_5.assets as assets
import dagster_testing.lesson_5.jobs as jobs
import dagster_testing.lesson_5.resources as resources
import dagster_testing.lesson_5.schedules as schedules
import dagster_testing.lesson_5.sensors as sensors
from dagster_testing.lesson_5.definitions import defs


# Assets
def test_config_asset():
    config = assets.AssetConfig(number=5)
    assert assets.config_asset(config) == 5


def test_resource_asset():
    resource = resources.ExampleResource(api_key="ABC")
    assert assets.resource_asset(resource) == 5


def test_combine_asset():
    assert assets.combine_asset(10, 10) == 20


def test_final_asset():
    assert assets.final_asset(10) == 100


def test_partition_asset():
    context = dg.build_asset_context(partition_key="1")
    assert assets.partition_asset(context) == 1


# Asset Checks
def test_non_negative():
    asset_check_pass = assets.non_negative(10)
    assert asset_check_pass.passed
    asset_check_fail = assets.non_negative(-10)
    assert not asset_check_fail.passed


# Jobs
def test_jobs():
    assert jobs.my_job
    assert jobs.my_job_configured


def test_job_selection():
    assert jobs.my_job.selection == dg.AssetSelection.all() - dg.AssetSelection.assets(
        "partition_asset"
    )


def test_job_config():
    assert (
        jobs.my_job_configured.config["ops"]["config_asset"]["config"]["number"] == 10
    )


# Schedules
def test_schedule():
    assert schedules.my_schedule
    assert schedules.my_schedule.cron_schedule == "0 0 5 * *"
    assert schedules.my_schedule.job == jobs.my_job


# Sensors
def test_sensors():
    assert sensors.my_sensor


@patch("dagster_testing.lesson_5.sensors.check_for_new_files", return_value=[])
def test_sensor_skip(mock_check_new_files):
    instance = dg.DagsterInstance.ephemeral()
    context = dg.build_sensor_context(instance=instance)
    assert sensors.my_sensor(context).__next__() == dg.SkipReason("No new files found")


@patch(
    "dagster_testing.lesson_5.sensors.check_for_new_files", return_value=["test_file"]
)
def test_sensor_run(mock_check_new_files):
    instance = dg.DagsterInstance.ephemeral()
    context = dg.build_sensor_context(instance=instance)
    assert sensors.my_sensor(context).__next__() == dg.RunRequest(run_key="test_file")


# Definitions
def test_def():
    assert defs


def test_def_objects():
    assert defs.get_assets_def("combine_asset")
    assert defs.get_job_def("jobs_config")
    assert defs.get_schedule_def("my_schedule")
    assert defs.get_sensor_def("my_sensor")
