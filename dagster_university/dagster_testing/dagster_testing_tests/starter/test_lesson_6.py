import pytest

import dagster_testing.starter.lesson_6.jobs as jobs  # noqa: F401
import dagster_testing.starter.lesson_6.schedules as schedules  # noqa: F401
import dagster_testing.starter.lesson_6.sensors as sensors  # noqa: F401
from dagster_testing.starter.lesson_6.definitions import defs


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


# Asset Checks
def test_non_negative():
    pass


# Jobs
def test_jobs():
    pass


def test_job_selection():
    pass


def test_job_config():
    pass


# Schedules
def test_schedule():
    pass


# Sensors
def test_sensors():
    pass


def test_sensor_skip():
    pass


def test_sensor_run():
    pass


# Definitions
def test_def():
    assert defs


def test_def_objects():
    pass
