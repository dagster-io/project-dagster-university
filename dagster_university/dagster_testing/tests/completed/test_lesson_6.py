import importlib
from pathlib import Path
from unittest.mock import patch

import dagster as dg
import pytest

import dagster_testing.defs
import dagster_testing.defs.jobs as jobs
import dagster_testing.defs.resources as resources
import dagster_testing.defs.schedules as schedules
import dagster_testing.defs.sensors as sensors
from dagster_testing.defs.assets import lesson_6


@pytest.fixture()
def defs():
    return dg.components.load_defs(dagster_testing.defs)


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


# Blocking Asset Checks
def test_validate_schema_pass():
    """Test that schema validation passes with correct columns."""
    valid_data = [{"City": "New York", "Population": "8804190"}]
    result = lesson_6.validate_schema(valid_data)
    assert result.passed
    assert "City" in result.metadata["actual_columns"].value
    assert "Population" in result.metadata["actual_columns"].value


def test_validate_schema_fail():
    """Test that schema validation fails with missing columns."""
    invalid_data = [{"Name": "New York", "Count": "8804190"}]
    result = lesson_6.validate_schema(invalid_data)
    assert not result.passed


# Asset Checks with Severity
def test_row_count_check_error():
    """Test that empty data returns ERROR severity."""
    result = lesson_6.row_count_check([])
    assert not result.passed
    assert result.severity == dg.AssetCheckSeverity.ERROR
    assert result.metadata["row_count"].value == 0


def test_row_count_check_warn():
    """Test that low row count returns WARN severity but still passes."""
    low_data = [{"City": "A", "Population": "1"}, {"City": "B", "Population": "2"}]
    result = lesson_6.row_count_check(low_data)
    assert result.passed  # Warning still passes
    assert result.severity == dg.AssetCheckSeverity.WARN
    assert result.metadata["row_count"].value == 2


def test_row_count_check_pass():
    """Test that sufficient row count passes without warning."""
    good_data = [
        {"City": "A", "Population": "1"},
        {"City": "B", "Population": "2"},
        {"City": "C", "Population": "3"},
    ]
    result = lesson_6.row_count_check(good_data)
    assert result.passed
    assert result.metadata["row_count"].value == 3


# Multi-Asset Checks
def test_population_data_checks():
    """Test multi-asset check runs multiple validations."""
    test_data = [
        {"City": "New York", "Population": "8804190"},
        {"City": "Buffalo", "Population": "278349"},
    ]

    results = list(lesson_6.population_data_checks(test_data))

    assert len(results) == 2

    # Check has_cities result
    cities_result = next(r for r in results if r.check_name == "has_cities")
    assert cities_result.passed
    assert cities_result.metadata["missing_count"].value == 0

    # Check has_populations result
    pop_result = next(r for r in results if r.check_name == "has_populations")
    assert pop_result.passed
    assert pop_result.metadata["missing_count"].value == 0


def test_population_data_checks_missing_data():
    """Test multi-asset check detects missing data."""
    test_data = [
        {"City": "New York", "Population": "8804190"},
        {"City": "", "Population": "278349"},  # Empty city
    ]

    results = list(lesson_6.population_data_checks(test_data))

    # has_cities should fail (empty string is falsy)
    cities_result = next(r for r in results if r.check_name == "has_cities")
    assert not cities_result.passed
    assert cities_result.metadata["missing_count"].value == 1


# Factory Pattern Asset Checks
def test_city_not_null_check():
    """Test factory-generated City not-null check."""
    # Test passing case
    valid_data = [{"City": "New York", "Population": "8804190"}]
    result = lesson_6.city_not_null_check(valid_data)
    assert result.passed
    assert result.metadata["null_count"].value == 0

    # Test failing case
    invalid_data = [{"City": None, "Population": "8804190"}]
    result = lesson_6.city_not_null_check(invalid_data)
    assert not result.passed
    assert result.metadata["null_count"].value == 1


def test_population_not_null_check():
    """Test factory-generated Population not-null check."""
    # Test passing case
    valid_data = [{"City": "New York", "Population": "8804190"}]
    result = lesson_6.population_not_null_check(valid_data)
    assert result.passed

    # Test failing case
    invalid_data = [{"City": "New York", "Population": None}]
    result = lesson_6.population_not_null_check(invalid_data)
    assert not result.passed


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
        == "tests/data/test.csv"
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
def test_defs(defs):
    assert defs


# Access assets
def test_square_asset(defs):
    _asset = defs.get_assets_def("squared")
    assert _asset(5) == 25


def test_square_key_asset(defs):
    _asset = defs.get_assets_def(dg.AssetKey(["target", "main", "square_key"]))
    assert _asset(5) == 25
