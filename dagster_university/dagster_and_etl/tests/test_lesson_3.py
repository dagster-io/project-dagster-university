import csv
import tempfile
from pathlib import Path
from unittest.mock import MagicMock

import dagster as dg
import pytest
from dagster_duckdb import DuckDBResource

import src.dagster_and_etl.completed.lesson_3.defs.assets as assets


@pytest.fixture()
def config_file():
    return Path(__file__).absolute().parent / "../data/source/2018-01-22.csv"


@pytest.fixture()
def duckdb_resource():
    return {
        "database": DuckDBResource(
            database="data/staging/data.duckdb",
        )
    }


@pytest.fixture()
def duckdb_mock_resource():
    mock_conn = MagicMock()
    mock_conn.execute = MagicMock()

    mock_db = MagicMock()
    mock_db.get_connection.return_value.__enter__.return_value = mock_conn
    return {"database": mock_db}


def test_import_file_assets(duckdb_resource):
    _assets = [
        assets.import_file,
        assets.duckdb_table,
    ]
    result = dg.materialize(
        assets=_assets,
        resources=duckdb_resource,
        run_config=dg.RunConfig(
            {
                "import_file": assets.IngestionFileConfig(path="2018-01-22.csv"),
            }
        ),
    )
    assert result.success


def test_import_partition_file_assets(duckdb_resource):
    _assets = [
        assets.import_partition_file,
        assets.duckdb_partition_table,
    ]
    result = dg.materialize(
        assets=_assets,
        resources=duckdb_resource,
        partition_key="2018-01-22",
    )
    assert result.success


def test_import_dynamic_partition_file_assets(duckdb_resource):
    instance = dg.DagsterInstance.ephemeral()
    instance.add_dynamic_partitions("dynamic_partition", ["2018-01-22"])

    _assets = [
        assets.import_dynamic_partition_file,
        assets.duckdb_dynamic_partition_table,
    ]
    result = dg.materialize(
        assets=_assets,
        resources=duckdb_resource,
        partition_key="2018-01-22",
        instance=instance,
    )
    assert result.success


def test_invalid_share_price(config_file):
    asset_check_pass = assets.invalid_share_price(
        dg.build_asset_context(),
        import_file=config_file,
    )
    assert asset_check_pass.passed


def test_invalid_share_price_failure():
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
        writer = csv.DictWriter(
            temp_file,
            fieldnames=["date", "share_price", "amount", "spend", "shift", "spread"],
        )
        writer.writeheader()
        writer.writerow(
            {
                "date": "2018-01-22",
                "share_price": "0",  # Invalid share price
                "amount": "100",
                "spend": "1000",
                "shift": "0.1",
                "spread": "0.2",
            }
        )

    try:
        asset_check_fail = assets.invalid_share_price(
            dg.build_asset_context(),
            import_file=temp_file.name,
        )
        assert not asset_check_fail.passed
        assert "'share' is below 0" in asset_check_fail.metadata
    finally:
        Path(temp_file.name).unlink()


def test_asset_check_with_actual_data(config_file):
    asset_check_pass = assets.invalid_share_price(
        dg.build_asset_context(),
        import_file=config_file,
    )
    assert asset_check_pass.passed
    assert asset_check_pass.metadata == {}


def test_import_file_s3_assets(duckdb_mock_resource):
    _assets = [
        assets.import_file_s3,
        assets.duckdb_table_s3,
    ]
    result = dg.materialize(
        assets=_assets,
        resources=duckdb_mock_resource,
        run_config=dg.RunConfig(
            {
                "import_file_s3": assets.IngestionFileS3Config(
                    bucket="test-bucket",
                    path="source/2018-01-22.csv",
                ),
            }
        ),
    )
    assert result.success
