import dagster as dg
import pytest

import dagster_essentials.completed.lesson_5.defs


@pytest.fixture()
def defs():
    return dg.components.load_defs(dagster_essentials.completed.lesson_5.defs)


def test_assets(defs):
    assets = [
        defs.get_assets_def(dg.AssetKey(["taxi_trips_file"])),
        defs.get_assets_def(dg.AssetKey(["taxi_zones_file"])),
        defs.get_assets_def(dg.AssetKey(["taxi_trips"])),
        defs.get_assets_def(dg.AssetKey(["taxi_zones"])),
        defs.get_assets_def(dg.AssetKey(["trips_by_week"])),
        defs.get_assets_def(dg.AssetKey(["manhattan_stats"])),
        defs.get_assets_def(dg.AssetKey(["manhattan_map"])),
    ]
    result = dg.materialize(assets)
    assert result.success


def test_defs(defs):
    assert defs
