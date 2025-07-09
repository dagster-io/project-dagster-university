import dagster as dg
import pytest

import src.dagster_and_dbt.completed.lesson_5.defs
from tests.fixtures import setup_dbt_env  # noqa: F401


@pytest.mark.parametrize("setup_dbt_env", ["lesson_5"], indirect=True)
def test_dbt_assets(setup_dbt_env):  # noqa: F811
    from src.dagster_and_dbt.completed.lesson_5.defs.assets import dbt, metrics
    from src.dagster_and_dbt.completed.lesson_5.defs.resources import (
        database_resource,
        dbt_resource,
    )

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
    from src.dagster_and_dbt.completed.lesson_5.defs.jobs import trip_update_job

    assert trip_update_job


@pytest.mark.parametrize("setup_dbt_env", ["lesson_5"], indirect=True)
def test_defs(setup_dbt_env):  # noqa: F811
    assert dg.Definitions.merge(
        dg.components.load_defs(src.dagster_and_dbt.completed.lesson_5.defs)
    )
