import dagster as dg
import pytest

import dagster_and_etl.completed.lesson_6.defs
from tests.fixtures import docker_compose  # noqa: F401


@pytest.mark.integration
def test_sling_replication_config(docker_compose):  # noqa: F811
    import yaml

    import dagster_and_etl.completed.lesson_6.defs.assets as assets

    with open(assets.replication_config, "r") as f:
        config = yaml.safe_load(f)

    assert config["source"] == "MY_POSTGRES"
    assert config["target"] == "MY_DUCKDB"
    assert config["defaults"]["mode"] == "full-refresh"

    streams = config["streams"]
    assert "data.customers" in streams
    assert "data.products" in streams
    assert "data.orders" in streams

    # Verify orders incremental config
    assert streams["data.orders"]["mode"] == "incremental"
    assert streams["data.orders"]["primary_key"] == "order_id"
    assert streams["data.orders"]["update_key"] == "order_date"


@pytest.mark.integration
def test_postgres_sling_assets(docker_compose):  # noqa: F811
    import dagster_and_etl.completed.lesson_6.defs.assets as assets
    from dagster_and_etl.completed.lesson_6.defs.resources import sling

    result = dg.materialize(
        assets=[
            assets.postgres_sling_assets,
            assets.downstream_orders,
            assets.downstream_products,
            assets.downstream_orders_and_products,
        ],
        resources={
            "sling": sling,
        },
    )
    assert result.success


@pytest.mark.integration
def test_incremental_replication(docker_compose):  # noqa: F811
    import dagster_and_etl.completed.lesson_6.defs.assets as assets
    from dagster_and_etl.completed.lesson_6.defs.resources import sling

    result = dg.materialize(
        assets=[assets.postgres_sling_assets],
        resources={"sling": sling},
    )
    assert result.success

    # Second run - should use incremental mode for orders
    result = dg.materialize(
        assets=[assets.postgres_sling_assets],
        resources={"sling": sling},
    )
    assert result.success


@pytest.mark.integration
def test_defs():
    assert dg.Definitions.merge(
        dg.components.load_defs(dagster_and_etl.completed.lesson_6.defs)
    )
