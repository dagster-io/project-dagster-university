import datetime
from unittest.mock import Mock, patch

import dagster as dg
import pytest
from dagster_duckdb import DuckDBResource

import dagster_and_etl.completed.lesson_4.defs
import dagster_and_etl.completed.lesson_4.defs.assets as assets
from dagster_and_etl.completed.lesson_4.defs.resources import NASAResource
from tests.nasa_data import nasa_response


@pytest.fixture()
def defs():
    return dg.components.load_defs(dagster_and_etl.completed.lesson_4.defs)


@pytest.fixture()
def nasa_config():
    return assets.NasaDate(
        date="2025-04-01",
    )


@pytest.fixture()
def asteroid_response():
    return nasa_response


def test_asteroid_assets(nasa_config, asteroid_response):
    mocked_resource = Mock()
    mocked_resource.get_near_earth_asteroids.return_value = asteroid_response

    _assets = [
        assets.asteroids,
        assets.asteroids_file,
        assets.duckdb_table,
    ]
    result = dg.materialize(
        assets=_assets,
        resources={
            "nasa": mocked_resource,
            "database": DuckDBResource(
                database="data/staging/data.duckdb",
            ),
        },
        run_config=dg.RunConfig(
            {
                "asteroids": nasa_config,
            }
        ),
    )
    assert result.success

    mocked_resource.get_near_earth_asteroids.assert_called_once_with(
        start_date="2025-03-31",
        end_date="2025-04-01",
    )


def test_asteroid_partition_assets(asteroid_response):
    mocked_resource = Mock()
    mocked_resource.get_near_earth_asteroids.return_value = asteroid_response

    _assets = [
        assets.asteroids_partition,
    ]
    result = dg.materialize(
        assets=_assets,
        resources={"nasa": mocked_resource},
        partition_key="2025-04-01",
    )
    assert result.success

    mocked_resource.get_near_earth_asteroids.assert_called_once_with(
        start_date="2025-03-31",
        end_date="2025-04-01",
    )


def test_nasa_date_validation():
    valid_config = assets.NasaDate(date="2025-04-01")
    assert valid_config.date == "2025-04-01"

    with pytest.raises(ValueError, match="event_date must be in 'YYYY-MM-DD' format"):
        assets.NasaDate(date="2025/04/01")

    with pytest.raises(ValueError):
        assets.NasaDate(date="2025-13-01")


def test_duckdb_table_data_verification(asteroid_response):
    mocked_resource = Mock()
    mocked_resource.get_near_earth_asteroids.return_value = asteroid_response

    _assets = [
        assets.asteroids,
        assets.asteroids_file,
        assets.duckdb_table,
    ]
    result = dg.materialize(
        assets=_assets,
        resources={
            "nasa": mocked_resource,
            "database": DuckDBResource(
                database="data/staging/data.duckdb",
            ),
        },
        run_config=dg.RunConfig(
            {
                "asteroids": assets.NasaDate(date="2025-04-01"),
            }
        ),
    )
    assert result.success

    # Verify data in database
    with DuckDBResource(database="data/staging/data.duckdb").get_connection() as conn:
        table_info = conn.execute("DESCRIBE raw_asteroid_data").fetchall()
        assert len(table_info) == 4  # Four columns
        assert any(col[0] == "id" for col in table_info)
        assert any(col[0] == "name" for col in table_info)
        assert any(col[0] == "absolute_magnitude_h" for col in table_info)
        assert any(col[0] == "is_potentially_hazardous_asteroid" for col in table_info)

        row_count = conn.execute("SELECT COUNT(*) FROM raw_asteroid_data").fetchone()[0]
        assert row_count > 0


def test_asteroid_partition_multiple_days(asteroid_response):
    mocked_resource = Mock()
    mocked_resource.get_near_earth_asteroids.return_value = asteroid_response

    _assets = [
        assets.asteroids_partition,
    ]

    partition_keys = ["2025-04-01", "2025-04-02", "2025-04-03"]
    for partition_key in partition_keys:
        result = dg.materialize(
            assets=_assets,
            resources={"nasa": mocked_resource},
            partition_key=partition_key,
        )
        assert result.success

        expected_start = (
            datetime.datetime.strptime(partition_key, "%Y-%m-%d")
            - datetime.timedelta(days=1)
        ).strftime("%Y-%m-%d")
        mocked_resource.get_near_earth_asteroids.assert_called_with(
            start_date=expected_start,
            end_date=partition_key,
        )


def test_asteroid_api_error_handling():
    mocked_resource = Mock()
    mocked_resource.get_near_earth_asteroids.side_effect = Exception("API Error")

    _assets = [
        assets.asteroids,
    ]
    with pytest.raises(Exception, match="API Error"):
        dg.materialize(
            assets=_assets,
            resources={"nasa": mocked_resource},
            run_config=dg.RunConfig(
                {
                    "asteroids": assets.NasaDate(date="2025-04-01"),
                }
            ),
        )


def test_defs(defs):
    assert defs


# Resource tests
def test_nasa_resource_initialization():
    """Test that NASA resource initializes correctly with API key."""
    resource = NASAResource(api_key="test_key")
    assert resource.api_key == "test_key"


@pytest.fixture()
def mock_session():
    """Create a mock requests session for testing retries."""
    with patch("requests.Session") as mock_session_class:
        mock_session_instance = Mock()
        mock_session_class.return_value = mock_session_instance
        yield mock_session_instance


def test_nasa_resource_api_call(mock_session, asteroid_response):
    """Test that NASA resource makes correct API calls."""
    mock_response = Mock()
    mock_response.json.return_value = {
        "near_earth_objects": {"2025-04-01": asteroid_response}
    }
    mock_response.raise_for_status.return_value = None
    mock_session.get.return_value = mock_response

    resource = NASAResource(api_key="test_key")
    result = resource.get_near_earth_asteroids("2025-04-01", "2025-04-02")

    assert result == asteroid_response
    mock_session.get.assert_called_once()
    mock_response.raise_for_status.assert_called_once()


def test_nasa_resource_api_error():
    """Test that NASA resource raises errors for failed requests."""
    from requests.exceptions import HTTPError

    with patch("requests.Session") as mock_session_class:
        mock_session_instance = Mock()
        mock_session_class.return_value = mock_session_instance

        mock_response = Mock()
        mock_response.raise_for_status.side_effect = HTTPError("404 Not Found")
        mock_session_instance.get.return_value = mock_response

        resource = NASAResource(api_key="test_key")
        with pytest.raises(HTTPError):
            resource.get_near_earth_asteroids("2025-04-01", "2025-04-02")
