import dagster as dg
import pytest

import dagster_essentials.completed.lesson_3.defs


@pytest.fixture()
def defs():
    return dg.components.load_defs(dagster_essentials.completed.lesson_3.defs)


def test_assets(defs):
    assets = [
        defs.get_assets_def(dg.AssetKey(["taxi_trips_file"])),
        defs.get_assets_def(dg.AssetKey(["taxi_zones_file"])),
    ]
    result = dg.materialize(assets)
    assert result.success


def test_defs(defs):
    assert defs
