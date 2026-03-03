from unittest.mock import MagicMock

import dagster as dg
import pytest

from ai_driven_data_engineering.defs.assets.trending_events import trending_events

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
    """Mock NewsApiResource that returns sample events."""
    mock_client = MagicMock()
    mock_client.execQuery.return_value = {"events": {"results": _SAMPLE_EVENTS}}
    mock_resource = MagicMock()
    mock_resource.get_client.return_value = mock_client
    return mock_resource


@pytest.fixture
def empty_mock_newsapi():
    """Mock NewsApiResource that returns no events."""
    mock_client = MagicMock()
    mock_client.execQuery.return_value = {}
    mock_resource = MagicMock()
    mock_resource.get_client.return_value = mock_client
    return mock_resource


def test_trending_events_materialize(duckdb_resource, mock_newsapi):
    """trending_events asset can be materialized with a mocked NewsAPI."""
    context = dg.build_asset_context(partition_key=_PARTITION_DATE)
    result = trending_events(context, duckdb_resource, mock_newsapi)
    assert isinstance(result, dg.MaterializeResult)


def test_trending_events_row_count(duckdb_resource, mock_newsapi):
    """trending_events reports correct row_count in materialization metadata."""
    context = dg.build_asset_context(partition_key=_PARTITION_DATE)
    result = trending_events(context, duckdb_resource, mock_newsapi)
    assert result.metadata["row_count"].value == len(_SAMPLE_EVENTS)


def test_trending_events_empty_response(duckdb_resource, empty_mock_newsapi):
    """trending_events handles an empty API response without error."""
    context = dg.build_asset_context(partition_key=_PARTITION_DATE)
    result = trending_events(context, duckdb_resource, empty_mock_newsapi)
    assert result.metadata["row_count"].value == 0


def test_trending_events_partition_isolation(duckdb_resource, mock_newsapi):
    """Re-materializing a partition replaces existing rows rather than appending."""
    for _ in range(2):
        context = dg.build_asset_context(partition_key=_PARTITION_DATE)
        result = trending_events(context, duckdb_resource, mock_newsapi)

    assert result.metadata["row_count"].value == len(_SAMPLE_EVENTS)
