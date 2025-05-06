from pathlib import Path
from unittest.mock import patch

import dagster as dg
import pytest

import dagster_testing.defs.jobs as jobs
import dagster_testing.defs.resources as resources
import dagster_testing.defs.schedules as schedules
import dagster_testing.defs.sensors as sensors
from dagster_testing.definitions import defs
from dagster_testing.defs.assets import lesson_6


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
def test_population_file_config():
    file_path = Path(__file__).absolute().parent / "../data/test.csv"

    config = lesson_6.FilepathConfig(path=file_path.as_posix())
    assert lesson_6.population_file_config(config) == [
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


def test_population_api_resource():
    result = lesson_6.population_api_resource(resources.StatePopulation())
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


def test_population_combined():
    population_file_config = [{"Population": 10}]
    population_api_resource = [
        {"Population": 20},
        {"Population": 40},
    ]
    assert (
        lesson_6.population_combined(population_file_config, population_api_resource)
        == 70
    )


def test_population_file_partition(file_output):
    context = dg.build_asset_context(partition_key="ny.csv")
    assert lesson_6.population_file_partition(context) == file_output


def test_total_population_partition(file_output):
    assert lesson_6.total_population_partition(file_output) == 9294108


# Asset Checks
def test_non_negative():
    asset_check_pass = lesson_6.non_negative(10)
    assert asset_check_pass.passed
    asset_check_fail = lesson_6.non_negative(-10)
    assert not asset_check_fail.passed


# Jobs
def test_jobs():
    assert jobs.my_job
    assert jobs.my_job_configured


def test_job_selection():
    _assets = [
        lesson_6.population_file_config,
        lesson_6.population_api_resource,
        lesson_6.population_combined,
    ]
    assert jobs.my_job.selection == dg.AssetSelection.assets(*_assets)


def test_job_config():
    assert (
        jobs.my_job_configured.config["ops"]["population_file_config"]["config"]["path"]
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


@patch("dagster_testing.defs.sensors.check_for_new_files", return_value=[])
def test_sensor_skip(mock_check_new_files):
    instance = dg.DagsterInstance.ephemeral()
    context = dg.build_sensor_context(instance=instance)
    assert sensors.my_sensor(context).__next__() == dg.SkipReason("No new files found")


@patch(
    "dagster_testing.defs.sensors.check_for_new_files",
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
