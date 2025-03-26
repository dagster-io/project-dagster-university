import pytest
from dagster_components import load_defs

from dagster_and_dbt_tests.fixtures import setup_dbt_env  # noqa: F401


@pytest.mark.parametrize("setup_dbt_env", ["lesson_8"], indirect=True)
def test_components_def_can_load(setup_dbt_env):  # noqa: F811
    import dagster_and_dbt.completed.lesson_8.components.defs

    assert load_defs(dagster_and_dbt.completed.lesson_8.components.defs)
