import datetime
from pathlib import Path
from unittest.mock import Mock

import dagster as dg
import pytest
from dagster_duckdb import DuckDBResource
from dotenv import dotenv_values

import dagster_and_etl.completed.lesson_4.defs
import dagster_and_etl.completed.lesson_4.defs.assets as assets
from dagster_and_etl.completed.lesson_4.defs.resources import NASAResource
from tests.nasa_data import nasa_response

_env_path = Path(__file__).parent.parent / ".env"
_real_api_key = dotenv_values(_env_path).get("NASA_API_KEY", "")


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


@pytest.fixture()
def real_nasa_resource():
    if not _real_api_key or _real_api_key == "DEMO_KEY":
        pytest.skip("Real NASA_API_KEY not found in .env")
    return NASAResource(api_key=_real_api_key)


@pytest.mark.integration
def test_nasa_resource_returns_asteroids(real_nasa_resource):
    data = real_nasa_resource.get_near_earth_asteroids(
        start_date="2025-04-01",
        end_date="2025-04-02",
    )
    assert isinstance(data, list)
    assert len(data) > 0
    expected_fields = {
        "id",
        "name",
        "absolute_magnitude_h",
        "is_potentially_hazardous_asteroid",
    }
    assert expected_fields.issubset(data[0].keys())


@pytest.mark.integration
def test_full_pipeline_end_to_end(real_nasa_resource, tmp_path):
    test_db = str(tmp_path / "test.duckdb")

    result = dg.materialize(
        assets=[assets.asteroids, assets.asteroids_file, assets.duckdb_table],
        resources={
            "nasa": real_nasa_resource,
            "database": DuckDBResource(database=test_db),
        },
        run_config=dg.RunConfig({"asteroids": assets.NasaDate(date="2025-04-02")}),
    )
    assert result.success

    with DuckDBResource(database=test_db).get_connection() as conn:
        count = conn.execute("SELECT COUNT(*) FROM raw_asteroid_data").fetchone()[0]
        assert count > 0


@pytest.mark.integration
def test_partitioned_asset_end_to_end(real_nasa_resource):
    result = dg.materialize(
        assets=[assets.asteroids_partition],
        resources={"nasa": real_nasa_resource},
        partition_key="2025-04-02",
    )
    assert result.success
    output = result.output_for_node("asteroids_partition")
    assert isinstance(output, list)
    assert len(output) > 0
