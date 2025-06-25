import dagster as dg
import pytest

from tests.fixtures import setup_dbt_env  # noqa: F401


@pytest.mark.parametrize("setup_dbt_env", ["lesson_6"], indirect=True)
def test_dbt_partitioned_incremental_assets(setup_dbt_env):  # noqa: F811
    from src.dagster_and_dbt.completed.lesson_6.defs.assets import dbt
    from src.dagster_and_dbt.completed.lesson_6.defs.resources import dbt_resource

    dbt_analytics_assets = dg.load_assets_from_modules(modules=[dbt])

    result = dg.materialize(
        assets=[*dbt_analytics_assets],
        resources={
            "dbt": dbt_resource,
        },
        partition_key="2023-01-01",
    )
    assert result.success
