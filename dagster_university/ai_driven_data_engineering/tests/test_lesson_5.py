from unittest.mock import MagicMock

import dagster as dg
import pytest

from ai_driven_data_engineering.completed.lesson_5.defs.assets import raw_data
from ai_driven_data_engineering.completed.lesson_5.defs.assets.trending_events import (
    trending_events,
)
from ai_driven_data_engineering.completed.lesson_5.defs.schedules import daily_raw

_PARTITION_DATE = "2024-01-15"

_SAMPLE_EVENTS = [
    {
        "uri": "event-123",
        "title": {"eng": "Test Event Title"},
        "summary": {"eng": "Test event summary text."},
        "eventDate": _PARTITION_DATE,
        "totalArticleCount": 42,
        "concepts": [
            {"label": {"eng": "Technology"}},
            {"label": {"eng": "Science"}},
        ],
    },
    {
        "uri": "event-456",
        "title": "Plain string title",
        "summary": "Plain string summary.",
        "eventDate": _PARTITION_DATE,
        "totalArticleCount": 10,
        "concepts": [],
    },
]


@pytest.fixture
def mock_newsapi():
    mock_client = MagicMock()
    mock_client.execQuery.return_value = {"events": {"results": _SAMPLE_EVENTS}}
    mock_resource = MagicMock()
    mock_resource.get_client.return_value = mock_client
    return mock_resource


@pytest.fixture
def empty_mock_newsapi():
    mock_client = MagicMock()
    mock_client.execQuery.return_value = {}
    mock_resource = MagicMock()
    mock_resource.get_client.return_value = mock_client
    return mock_resource


# --- raw assets ---


def test_raw_assets_materialize(duckdb_resource):
    result = dg.materialize(
        assets=[
            raw_data.raw_customers,
            raw_data.raw_orders,
            raw_data.raw_payments,
        ],
        resources={"duckdb": duckdb_resource},
    )
    assert result.success

    for node_name in ["raw_customers", "raw_orders", "raw_payments"]:
        materializations = result.asset_materializations_for_node(node_name)
        assert len(materializations) > 0
        assert "row_count" in materializations[0].metadata


def test_raw_customers_row_count(duckdb_resource):
    result = dg.materialize(
        assets=[raw_data.raw_customers],
        resources={"duckdb": duckdb_resource},
    )
    assert result.success
    materializations = result.asset_materializations_for_node("raw_customers")
    row_count = materializations[0].metadata["row_count"].value
    assert row_count > 0


# --- schedule ---


def test_raw_ingestion_job_exists():
    assert daily_raw.raw_ingestion_job is not None
    assert daily_raw.raw_ingestion_job.name == "raw_ingestion_job"


def test_daily_raw_schedule_exists():
    assert daily_raw.daily_raw_schedule is not None
    assert daily_raw.daily_raw_schedule.name == "daily_raw_8am_est"
    assert daily_raw.daily_raw_schedule.cron_schedule == "0 8 * * *"
    assert daily_raw.daily_raw_schedule.execution_timezone == "America/New_York"
    assert daily_raw.daily_raw_schedule.job == daily_raw.raw_ingestion_job


def test_trending_events_job_exists():
    assert daily_raw.trending_events_job is not None
    assert daily_raw.trending_events_job.name == "trending_events_job"


def test_daily_trending_events_schedule_exists():
    assert daily_raw.daily_trending_events_schedule is not None
    assert (
        daily_raw.daily_trending_events_schedule.name == "daily_trending_events_8am_est"
    )
    assert daily_raw.daily_trending_events_schedule.cron_schedule == "0 8 * * *"


# --- trending events ---


def test_trending_events_materialize(duckdb_resource, mock_newsapi):
    context = dg.build_asset_context(partition_key=_PARTITION_DATE)
    result = trending_events(context, duckdb_resource, mock_newsapi)
    assert isinstance(result, dg.MaterializeResult)


def test_trending_events_row_count(duckdb_resource, mock_newsapi):
    context = dg.build_asset_context(partition_key=_PARTITION_DATE)
    result = trending_events(context, duckdb_resource, mock_newsapi)
    assert result.metadata["row_count"].value == len(_SAMPLE_EVENTS)


def test_trending_events_empty_response(duckdb_resource, empty_mock_newsapi):
    context = dg.build_asset_context(partition_key=_PARTITION_DATE)
    result = trending_events(context, duckdb_resource, empty_mock_newsapi)
    assert result.metadata["row_count"].value == 0


def test_trending_events_partition_isolation(duckdb_resource, mock_newsapi):
    for _ in range(2):
        context = dg.build_asset_context(partition_key=_PARTITION_DATE)
        result = trending_events(context, duckdb_resource, mock_newsapi)
    assert result.metadata["row_count"].value == len(_SAMPLE_EVENTS)
