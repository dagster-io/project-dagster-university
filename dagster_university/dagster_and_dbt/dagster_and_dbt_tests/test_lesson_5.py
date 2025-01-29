import dagster as dg

from dagster_and_dbt.lesson_4.definitions import defs
from dagster_and_dbt.lesson_5.assets import dbt, metrics
from dagster_and_dbt.lesson_5.jobs import trip_update_job
from dagster_and_dbt.lesson_5.resources import database_resource, dbt_resource

dbt_analytics_assets = dg.load_assets_from_modules(modules=[dbt])


def test_dbt_assets():
    result = dg.materialize(
        assets=[metrics.airport_trips, *dbt_analytics_assets],
        resources={
            "database": database_resource,
            "dbt": dbt_resource,
        },
    )
    assert result.success


def test_jobs():
    assert trip_update_job


def test_def_can_load():
    assert defs