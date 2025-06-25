import pytest

import src.dagster_testing.defs.jobs as jobs  # noqa: F401
import src.dagster_testing.defs.schedules as schedules  # noqa: F401
import src.dagster_testing.defs.sensors as sensors  # noqa: F401
from src.dagster_testing.definitions import defs
from src.dagster_testing.defs.assets import lesson_6  # noqa: F401


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
