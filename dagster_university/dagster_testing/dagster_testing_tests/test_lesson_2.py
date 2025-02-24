from pathlib import Path

import dagster as dg
import pytest
import yaml
from dagster._core.errors import DagsterTypeCheckDidNotPass

from dagster_testing.lesson_2.assets import (
    FilepathConfig,
    func_wrong_type,
    loaded_file,
    loaded_file_config,
    loaded_file_logging,
    partition_asset_letter,
    partition_asset_number,
    processed_file,
    processed_file_config,
    processed_file_meta,
    processed_file_meta_yield,
    wrong_type_annotation,
)
from dagster_testing.lesson_2.definitions import defs


@pytest.fixture()
def test_file():
    return "path.txt"


def test_loaded_file():
    assert loaded_file() == "  contents  "


def test_processed_file():
    assert processed_file(" contents  ") == "contents"


def test_processed_file_meta():
    result = processed_file_meta(" contents  ")
    assert result == dg.MaterializeResult(
        asset_key=None, metadata={"file_content": "contents"}
    )


def test_processed_file_meta_yield():
    result = processed_file_meta_yield(" contents  ")
    assert result.__next__() == dg.MaterializeResult(
        asset_key=None, metadata={"file_content": "contents"}
    )


def test_func_wrong_type():
    assert func_wrong_type() == 2


# Test intended to fail
@pytest.mark.skip
def test_wrong_type_annotation():
    assert wrong_type_annotation() == 2


def test_wrong_type_annotation_error():
    with pytest.raises(DagsterTypeCheckDidNotPass):
        wrong_type_annotation()


def test_assets():
    assets = [
        loaded_file,
        processed_file,
    ]
    result = dg.materialize(assets)
    assert result.success

    result.output_for_node("loaded_file") == "  contents  "
    result.output_for_node("processed_file") == "contents"


def test_loaded_file_config():
    config = FilepathConfig(path="path.txt")
    loaded_file_config(config) == "  example  "


@pytest.fixture()
def example_config():
    return FilepathConfig(path="path.txt")


def test_loaded_file_config_fixture(example_config):
    loaded_file_config(example_config) == "  example  "


def test_assets_config():
    assets = [
        loaded_file_config,
        processed_file_config,
    ]
    result = dg.materialize(
        assets=assets,
        run_config=dg.RunConfig(
            {"loaded_file_config": FilepathConfig(path="path.txt")}
        ),
    )
    assert result.success

    result.output_for_node("loaded_file_config") == "  example  "
    result.output_for_node("processed_file_config") == "example"


def test_assets_config_yaml():
    assets = [
        loaded_file_config,
        processed_file_config,
    ]
    result = dg.materialize(
        assets=assets,
        run_config=yaml.safe_load(
            (Path(__file__).absolute().parent / "configs/lesson_2.yaml").open()
        ),
    )
    assert result.success

    result.output_for_node("loaded_file_config") == "  example  "
    result.output_for_node("processed_file_config") == "example"


# Test intended to fail
@pytest.mark.skip
def test_loaded_file_logging_no_context():
    result = loaded_file_logging()
    assert result == "  contents  "


def test_loaded_file_logging():
    context = dg.build_asset_context()
    result = loaded_file_logging(context)
    assert result == "  contents  "


def test_assets_context():
    result = dg.materialize(
        assets=[loaded_file_logging],
    )
    assert result.success

    result.output_for_node("loaded_file_logging") == "  example  "


def test_partition_asset_number() -> None:
    context = dg.build_asset_context(partition_key="1")
    assert partition_asset_number(context) == 1


def test_assets_partition() -> None:
    result = dg.materialize(
        assets=[
            partition_asset_number,
        ],
        partition_key="1",
    )
    assert result.success

    result.output_for_node("partition_asset_number") == 1


# Test intended to fail
@pytest.mark.skip
def test_assets_multiple_partition() -> None:
    result = dg.materialize(
        assets=[
            partition_asset_number,
            partition_asset_letter,
        ],
        partition_key="1",
    )
    assert result.success

    result.output_for_node("partition_asset_letter") == 1
    result.output_for_node("partition_asset_letter") == "A"


def test_def():
    assert defs
