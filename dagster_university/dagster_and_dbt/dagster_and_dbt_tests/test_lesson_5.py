import dagster as dg
import pytest

from dagster_and_dbt_tests.fixtures import setup_dbt_env  # noqa: F401


@pytest.mark.parametrize("setup_dbt_env", ["lesson_5"], indirect=True)
def test_dbt_assets(setup_dbt_env):  # noqa: F811
    from dagster_and_dbt.lesson_5.assets import dbt, metrics
    from dagster_and_dbt.lesson_5.resources import database_resource, dbt_resource

    dbt_analytics_assets = dg.load_assets_from_modules(modules=[dbt])

    result = dg.materialize(
        assets=[metrics.airport_trips, *dbt_analytics_assets],
        resources={
            "database": database_resource,
            "dbt": dbt_resource,
        },
    )
    assert result.success


@pytest.mark.parametrize("setup_dbt_env", ["lesson_5"], indirect=True)
def test_jobs(setup_dbt_env):  # noqa: F811
    from dagster_and_dbt.lesson_5.jobs import trip_update_job

    assert trip_update_job


@pytest.mark.parametrize("setup_dbt_env", ["lesson_5"], indirect=True)
def test_def_can_load(setup_dbt_env):  # noqa: F811
    from dagster_and_dbt.lesson_4.definitions import defs

    assert defs
