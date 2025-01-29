from pathlib import Path

import dagster as dg

from dagster_and_dbt.lesson_3.assets import dbt
from dagster_and_dbt.lesson_3.definitions import defs
from dagster_and_dbt.lesson_3.resources import database_resource, dbt_resource
from dagster_and_dbt_tests.utils import run_dbt_command

dbt_analytics_assets = dg.load_assets_from_modules(modules=[dbt])

LESSON_DIR = (
    Path(__file__).joinpath("..", "dagster_and_dbt", "lesson_3", "analytics").resolve()
)


def test_dbt_assets():
    run_dbt_command("parse", LESSON_DIR)

    result = dg.materialize(
        assets=[*dbt_analytics_assets],
        resources={
            "database": database_resource,
            "dbt": dbt_resource,
        },
    )
    assert result.success

def test_def_can_load():
    assert defs