import dagster as dg
import pytest
from dagster_dlt import DagsterDltResource

import dagster_and_etl.completed.lesson_5.defs.assets as assets
import dagster_and_etl.completed.lesson_5.dlt_nasa as dlt_nasa
import dagster_and_etl.completed.lesson_5.dlt_quick_start as dlt_quick_start
from dagster_and_etl.completed.lesson_5.definitions import defs


@pytest.fixture()
def nasa_config():
    return assets.NasaDateRange(
        start_date="2025-04-01",
        end_date="2025-04-02",
    )


def test_dlt_quick_start():
    load_info = dlt_quick_start.pipeline.run(dlt_quick_start.simple_source())
    assert load_info is not None


def test_dlt_nasa():
    load_info = dlt_nasa.pipeline.run(
        dlt_nasa.nasa_neo_source(
            start_date="2015-09-07",
            end_date="2015-09-08",
            api_key="DEMO_KEY",
        )
    )
    assert load_info is not None


def test_dlt_quick_start_assets():
    result = dg.materialize(
        assets=[
            assets.dlt_simple,
        ],
        resources={
            "dlt": DagsterDltResource(),
        },
    )
    assert result.success


def test_dlt_csv_assets():
    result = dg.materialize(
        assets=[
            assets.import_file,
            assets.dlt_load_csv,
        ],
        resources={
            "dlt": DagsterDltResource(),
        },
        run_config=dg.RunConfig(
            {
                "import_file": assets.FilePath(path="2018-01-22.csv"),
            }
        ),
    )
    assert result.success


def test_dlt_nasa_assets(nasa_config):
    result = dg.materialize(
        assets=[
            assets.dlt_nasa,
        ],
        resources={
            "dlt": DagsterDltResource(),
        },
        run_config=dg.RunConfig(
            {
                "dlt_nasa": nasa_config,
            }
        ),
    )
    assert result.success


def test_def_can_load():
    assert defs
