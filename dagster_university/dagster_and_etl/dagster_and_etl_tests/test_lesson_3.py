from pathlib import Path

import dagster as dg
import pytest
from dagster_duckdb import DuckDBResource

import dagster_and_etl.completed.lesson_3.defs as defs
import dagster_and_etl.completed.lesson_3.defs.assets as assets


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


def test_not_empty(config_file):
    asset_check_pass = assets.not_empty(
        dg.build_asset_context(),
        import_file=config_file,
    )
    assert asset_check_pass.passed


def test_def_can_load():
    assert defs
