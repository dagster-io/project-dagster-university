import dagster as dg
import pytest

import dagster_essentials.completed.lesson_6.defs
from dagster_essentials.completed.lesson_6.defs.resources import database_resource


@pytest.fixture()
def defs():
    return dg.components.load_defs(dagster_essentials.completed.lesson_6.defs)


def test_assets(defs):
    assets = [
        defs.get_assets_def(dg.AssetKey(["taxi_trips_file"])),
        defs.get_assets_def(dg.AssetKey(["taxi_zones_file"])),
        defs.get_assets_def(dg.AssetKey(["taxi_trips"])),
        defs.get_assets_def(dg.AssetKey(["taxi_zones"])),
        defs.get_assets_def(dg.AssetKey(["trips_by_week"])),
        defs.get_assets_def(dg.AssetKey(["manhattan", "manhattan_stats"])),
        defs.get_assets_def(dg.AssetKey(["manhattan_map"])),
    ]
    result = dg.materialize(
        assets=assets,
        resources={
            "database": database_resource,
        },
    )
    assert result.success


def test_defs(defs):
    assert defs
