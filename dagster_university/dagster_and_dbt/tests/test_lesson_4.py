import dagster as dg
import pytest

import src.dagster_and_dbt.completed.lesson_4.defs
from tests.fixtures import setup_dbt_env  # noqa: F401


@pytest.mark.parametrize("setup_dbt_env", ["lesson_4"], indirect=True)
def test_dbt_assets(setup_dbt_env):  # noqa: F811
    from src.dagster_and_dbt.completed.lesson_4.defs.assets import dbt
    from src.dagster_and_dbt.completed.lesson_4.defs.resources import dbt_resource

    dbt_analytics_assets = dg.load_assets_from_modules(modules=[dbt])

    result = dg.materialize(
        assets=[*dbt_analytics_assets],
        resources={
            "dbt": dbt_resource,
        },
    )
    assert result.success


@pytest.mark.parametrize("setup_dbt_env", ["lesson_4"], indirect=True)
def test_defs(setup_dbt_env):  # noqa: F811
    assert dg.Definitions.merge(
        dg.components.load_defs(src.dagster_and_dbt.completed.lesson_4.defs)
    )
