import dagster as dg
from dagster_and_dbt.lesson_4.assets import dbt
from dagster_and_dbt.lesson_4.definitions import defs
from dagster_and_dbt.lesson_4.resources import dbt_resource

dbt_analytics_assets = dg.load_assets_from_modules(modules=[dbt])


def test_dbt_assets():
    result = dg.materialize(
        assets=[*dbt_analytics_assets],
        resources={
            "dbt": dbt_resource,
        },
    )
    assert result.success


def test_def_can_load():
    assert defs