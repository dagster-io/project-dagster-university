from pathlib import Path
from unittest.mock import patch

import dagster as dg
import pytest

import dagster_testing.completed.lesson_6.assets as assets
import dagster_testing.completed.lesson_6.jobs as jobs
import dagster_testing.completed.lesson_6.resources as resources
import dagster_testing.completed.lesson_6.schedules as schedules
import dagster_testing.completed.lesson_6.sensors as sensors
from dagster_testing.completed.lesson_6.definitions import defs


@pytest.fixture()
def file_output():
    return [
        {
            "City": "New York",
            "Population": "8804190",
        },
        {
            "City": "Buffalo",
            "Population": "278349",
        },
        {
            "City": "Yonkers",
            "Population": "211569",
        },
    ]


# Assets
def test_state_population_file_config():
    file_path = Path(__file__).absolute().parent / "../data/test.csv"

    config = assets.FilepathConfig(path=file_path.as_posix())
    assert assets.state_population_file_config(config) == [
        {
            "City": "Example 1",
            "Population": "4500000",
        },
        {
            "City": "Example 2",
            "Population": "3000000",
        },
        {
            "City": "Example 3",
            "Population": "1000000",
        },
    ]


def test_state_population_api_resource():
    result = assets.state_population_api_resource(resources.StatePopulation())
    assert result == [
        {
            "City": "Milwaukee",
            "Population": 577222,
        },
        {
            "City": "Madison",
            "Population": 269840,
        },
    ]


def test_total_population():
    state_population_file_config = [{"Population": 10}]
    state_population_api_resource = [
        {"Population": 20},
        {"Population": 40},
    ]
    assert (
        assets.total_population(
            state_population_file_config, state_population_api_resource
        )
        == 70
    )


def test_state_population_file_partition(file_output):
    context = dg.build_asset_context(partition_key="ny.csv")
    assert assets.state_population_file_partition(context) == file_output


def test_total_population_partition(file_output):
    assert assets.total_population_partition(file_output) == 9294108


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
        "state_population_file_partition"
    ) - dg.AssetSelection.assets("total_population_partition")


def test_job_config():
    assert (
        jobs.my_job_configured.config["ops"]["state_population_file_config"]["config"][
            "path"
        ]
        == "dagster_testing_tests/data/test.csv"
    )


# Schedules
def test_schedule():
    assert schedules.my_schedule
    assert schedules.my_schedule.cron_schedule == "0 0 5 * *"
    assert schedules.my_schedule.job == jobs.my_job


# Sensors
def test_sensors():
    assert sensors.my_sensor


@patch(
    "dagster_testing.completed.lesson_6.sensors.check_for_new_files", return_value=[]
)
def test_sensor_skip(mock_check_new_files):
    instance = dg.DagsterInstance.ephemeral()
    context = dg.build_sensor_context(instance=instance)
    assert sensors.my_sensor(context).__next__() == dg.SkipReason("No new files found")


@patch(
    "dagster_testing.completed.lesson_6.sensors.check_for_new_files",
    return_value=["test_file"],
)
def test_sensor_run(mock_check_new_files):
    instance = dg.DagsterInstance.ephemeral()
    context = dg.build_sensor_context(instance=instance)
    assert sensors.my_sensor(context).__next__() == dg.RunRequest(run_key="test_file")


# Definitions
def test_def():
    assert defs


def test_def_objects():
    assert defs.get_assets_def("total_population")
    assert defs.get_job_def("jobs_config")
    assert defs.get_schedule_def("my_schedule")
    assert defs.get_sensor_def("my_sensor")
