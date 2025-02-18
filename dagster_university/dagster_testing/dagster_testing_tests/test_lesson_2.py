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
    processed_file,
    processed_file_config,
    wrong_type_annotation,
)


@pytest.fixture()
def test_file():
    return "path.txt"


def test_loaded_file():
    assert loaded_file() == "  contents  "


def test_processed_file():
    assert processed_file(" contents  ") == "contents"


def test_func_wrong_type():
    assert func_wrong_type() == 2


# def test_wrong_type_annotation():
#     assert wrong_type_annotation() == 2


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
        run_config=yaml.safe_load(
            (Path(__file__).absolute().parent / "lesson_2_run_config.yaml").open()
        ),
    )
    assert result.success

    result.output_for_node("loaded_file_config") == "  example  "
    result.output_for_node("processed_file_config") == "example"
