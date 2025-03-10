from unittest.mock import Mock, patch  # noqa: F401

import dagster as dg  # noqa: F401
import pytest

import dagster_testing.starter.lesson_4.assets as assets  # noqa: F401
from dagster_testing.starter.lesson_4.definitions import defs


@pytest.fixture
def example_response():
    return {
        "cities": [
            {
                "city_name": "New York",
                "city_population": 8804190,
            },
            {
                "city_name": "Buffalo",
                "city_population": 278349,
            },
        ],
    }


@pytest.fixture
def api_output():
    return [
        {
            "city": "New York",
            "population": 8804190,
        },
        {
            "city": "Buffalo",
            "population": 278349,
        },
    ]


@pytest.fixture
def fake_city():
    return {
        "city": "Fakestown",
        "population": 42,
    }


def test_state_population_api():
    pass


def test_state_population_api_resource_mock():
    pass


def test_state_population_api_assets():
    pass


def test_state_population_api_assets_config():
    pass


def test_state_population_api_mocked_resource():
    pass


def test_state_population_api_assets_mocked_resource():
    pass


def test_def():
    assert defs
