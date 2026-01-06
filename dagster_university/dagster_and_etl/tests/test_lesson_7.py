import dagster as dg
import pytest

import dagster_and_etl.completed.lesson_7.defs
from tests.fixtures import docker_compose  # noqa: F401


@pytest.fixture()
def defs():
    return dg.Definitions.merge(
        dg.components.load_defs(dagster_and_etl.completed.lesson_7.defs)
    )


@pytest.mark.integration
def test_postgres_component_sling_assets(defs, docker_compose):  # noqa: F811
    result = dg.materialize(
        assets=[
            defs.get_assets_def(dg.AssetKey(["target", "data", "customers"])),
            defs.get_assets_def(dg.AssetKey(["target", "data", "orders"])),
            defs.get_assets_def(dg.AssetKey(["target", "data", "products"])),
            defs.get_assets_def("downstream_orders"),
            defs.get_assets_def("downstream_products"),
            defs.get_assets_def("downstream_orders_and_products"),
        ],
    )
    assert result.success


@pytest.mark.integration
def test_defs(defs):
    assert defs
