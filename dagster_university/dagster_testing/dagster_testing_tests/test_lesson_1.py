import pytest
import yaml
from pathlib import Path

import dagster as dg
from dagster_testing.lesson_1.assets import (
    loaded_file,
    processed_file,
    FilepathConfig,
    loaded_file_config,
    processed_file_config,
)


@pytest.fixture()
def test_file():
    return "path.txt"


def test_loaded_file():
    assert loaded_file() == "  contents  "


def test_processed_file():
    assert processed_file(" contents  ") == "contents"


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
    loaded_file_config(config)


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
            (Path(__file__).absolute().parent / "lesson_1_run_config.yaml").open()
        ),
    )
    assert result.success

    result.output_for_node("loaded_file_config") == "  example  "
    result.output_for_node("processed_file_config") == "example"
