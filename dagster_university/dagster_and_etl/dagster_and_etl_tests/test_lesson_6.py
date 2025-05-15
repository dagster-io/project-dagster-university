import dagster as dg
import pytest

from dagster_and_etl_tests.fixtures import docker_compose  # noqa: F401


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
def test_def_can_load(docker_compose):  # noqa: F811
    from dagster_and_etl.completed.lesson_6.definitions import defs

    assert defs
