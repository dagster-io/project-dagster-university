import dagster as dg
from dagster_and_dbt.lesson_6.assets import dbt
from dagster_and_dbt.lesson_6.definitions import defs
from dagster_and_dbt.lesson_6.resources import dbt_resource

dbt_analytics_assets = dg.load_assets_from_modules(modules=[dbt])


def test_dbt_partitioned_incremental_assets():
    result = dg.materialize(
        assets=[*dbt_analytics_assets],
        resources={
            "dbt": dbt_resource,
        },
        partition_key="2023-01-01",
    )
    assert result.success


def test_def_can_load():
    assert defs