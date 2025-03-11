import dagster as dg
import pytest

from dagster_and_dbt_tests.fixtures import setup_dbt_env  # noqa: F401


@pytest.mark.parametrize("setup_dbt_env", ["lesson_4"], indirect=True)
def test_dbt_assets(setup_dbt_env):  # noqa: F811
    from dagster_and_dbt.completed.lesson_4.assets import dbt
    from dagster_and_dbt.completed.lesson_4.resources import dbt_resource

    dbt_analytics_assets = dg.load_assets_from_modules(modules=[dbt])

    result = dg.materialize(
        assets=[*dbt_analytics_assets],
        resources={
            "dbt": dbt_resource,
        },
    )
    assert result.success


@pytest.mark.parametrize("setup_dbt_env", ["lesson_4"], indirect=True)
def test_def_can_load(setup_dbt_env):  # noqa: F811
    from dagster_and_dbt.completed.lesson_4.definitions import defs

    assert defs
