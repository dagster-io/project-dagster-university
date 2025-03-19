from pathlib import Path

import dagster as dg
import pytest
from dagster_duckdb import DuckDBResource

import dagster_and_etl.completed.lesson_3.assets as assets
from dagster_and_etl.completed.lesson_3.definitions import defs


@pytest.fixture()
def config_file():
    return Path(__file__).absolute().parent / "../data/source/2018-01-22.csv"


def test_import_file_assets():
    _assets = [
        assets.import_file,
        assets.duckdb_table,
    ]
    result = dg.materialize(
        assets=_assets,
        resources={
            "database": DuckDBResource(
                database="data/staging/data.duckdb",
            ),
        },
        run_config=dg.RunConfig(
            {
                "import_file": assets.FilePath(path="2018-01-22.csv"),
            }
        ),
    )
    assert result.success


def test_not_empty(config_file):
    asset_check_pass = assets.not_empty(
        dg.build_asset_context(), import_file=config_file
    )
    assert asset_check_pass.passed


def test_import_partition_file_assets():
    _assets = [
        assets.import_partition_file,
        assets.duckdb_partition_table,
    ]
    result = dg.materialize(
        assets=_assets,
        resources={
            "database": DuckDBResource(
                database="data/staging/data.duckdb",
            ),
        },
        partition_key="2018-01-22",
    )
    assert result.success


def test_def_can_load():
    assert defs
