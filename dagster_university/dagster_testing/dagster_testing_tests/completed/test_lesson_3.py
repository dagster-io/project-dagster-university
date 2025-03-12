from pathlib import Path

import dagster as dg
import pytest
import yaml
from dagster._core.errors import DagsterTypeCheckDidNotPass

import dagster_testing.assets.unit_assets as unit_assets


@pytest.fixture()
def config_file():
    # Move up one directory to account for nesting of completed files
    file_path = Path(__file__).absolute().parent / "../data/test.csv"
    return unit_assets.FilepathConfig(path=file_path.as_posix())


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


@pytest.fixture()
def file_example_output():
    return [
        {
            "City": "Example 1",
            "Population": "4500000",
        },
        {
            "City": "Example 2",
            "Population": "3000000",
        },
        {
            "City": "Example 3",
            "Population": "1000000",
        },
    ]


@pytest.fixture()
def file_population():
    return 9294108


def test_state_population_file():
    assert unit_assets.state_population_file() == [
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


def test_total_population(file_output, file_population):
    assert unit_assets.total_population(file_output) == file_population


def test_total_population_meta(file_output, file_population):
    result = unit_assets.total_population_meta(file_output)
    assert result == dg.MaterializeResult(
        asset_key=None, metadata={"total_population": file_population}
    )


def test_total_population_meta_yield(file_output, file_population):
    result = unit_assets.total_population_meta_yield(file_output)
    assert result.__next__() == dg.MaterializeResult(
        asset_key=None, metadata={"total_population": file_population}
    )


def test_func_wrong_type():
    assert unit_assets.func_wrong_type() == 2


# Test intended to fail
@pytest.mark.skip
def test_wrong_type_annotation(file_output):
    assert unit_assets.total_population_wrong_type() == file_output


def test_wrong_type_annotation_error(file_output, file_population):
    with pytest.raises(DagsterTypeCheckDidNotPass):
        assert unit_assets.total_population_wrong_type(file_output) == file_population


def test_assets(file_output, file_population):
    _assets = [
        unit_assets.state_population_file,
        unit_assets.total_population,
    ]
    result = dg.materialize(_assets)
    assert result.success

    assert result.output_for_node("state_population_file") == file_output
    assert result.output_for_node("total_population") == file_population


def test_state_population_file_config():
    file_path = Path(__file__).absolute().parent / "../data/test.csv"

    config = unit_assets.FilepathConfig(path=file_path.as_posix())
    assert unit_assets.state_population_file_config(config) == [
        {
            "City": "Example 1",
            "Population": "4500000",
        },
        {
            "City": "Example 2",
            "Population": "3000000",
        },
        {
            "City": "Example 3",
            "Population": "1000000",
        },
    ]


def test_state_population_file_config_fixture_1(config_file):
    assert unit_assets.state_population_file_config(config_file) == [
        {
            "City": "Example 1",
            "Population": "4500000",
        },
        {
            "City": "Example 2",
            "Population": "3000000",
        },
        {
            "City": "Example 3",
            "Population": "1000000",
        },
    ]


def test_state_population_file_config_fixture_2(config_file, file_example_output):
    assert unit_assets.state_population_file_config(config_file) == file_example_output


def test_assets_config(config_file, file_example_output):
    _assets = [
        unit_assets.state_population_file_config,
        unit_assets.total_population_config,
    ]
    result = dg.materialize(
        assets=_assets,
        run_config=dg.RunConfig({"state_population_file_config": config_file}),
    )
    assert result.success

    assert result.output_for_node("state_population_file_config") == file_example_output
    assert result.output_for_node("total_population_config") == 8500000


def test_assets_config_yaml(file_example_output):
    _assets = [
        unit_assets.state_population_file_config,
        unit_assets.total_population_config,
    ]
    result = dg.materialize(
        assets=_assets,
        run_config=yaml.safe_load(
            (Path(__file__).absolute().parent / "../configs/lesson_3.yaml").open()
        ),
    )
    assert result.success

    assert result.output_for_node("state_population_file_config") == file_example_output
    assert result.output_for_node("total_population_config") == 8500000


# Test intended to fail
@pytest.mark.skip
def test_state_population_file_logging_no_context(file_output):
    result = unit_assets.state_population_file_logging()
    assert result == file_output


def test_state_population_file_logging(file_output):
    context = dg.build_asset_context()
    result = unit_assets.state_population_file_logging(context)
    assert result == file_output


def test_assets_context(file_output):
    result = dg.materialize(
        assets=[unit_assets.state_population_file_logging],
    )
    assert result.success

    assert result.output_for_node("state_population_file_logging") == file_output


def test_state_population_file_partition(file_output):
    context = dg.build_asset_context(partition_key="ny.csv")
    assert unit_assets.state_population_file_partition(context) == file_output


def test_assets_partition(file_output):
    result = dg.materialize(
        assets=[
            unit_assets.state_population_file_partition,
        ],
        partition_key="ny.csv",
    )
    assert result.success

    assert result.output_for_node("state_population_file_partition") == file_output


# Test intended to fail
@pytest.mark.skip
def test_assets_multiple_partition() -> None:
    result = dg.materialize(
        assets=[
            unit_assets.state_population_file_partition,
            unit_assets.partition_asset_letter,
        ],
        partition_key="ny.csv",
    )
    assert result.success

    result.output_for_node("state_population_file_partition") == 1
    result.output_for_node("partition_asset_letter") == "A"
