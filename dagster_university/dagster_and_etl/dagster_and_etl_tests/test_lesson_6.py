import dagster as dg
import pytest
from dagster_dlt import DagsterDltResource

from dagster_and_etl_tests.fixtures import docker_compose  # noqa: F401


@pytest.mark.integration
def test_dlt_postgres_assets(docker_compose):  # noqa: F811
    from dagster_and_etl.completed.lesson_6.defs.assets import dlt_postgres_assets

    result = dg.materialize(
        assets=[dlt_postgres_assets],
        resources={
            "dlt": DagsterDltResource(),
        },
    )
    assert result.success


@pytest.mark.integration
def test_def_can_load(docker_compose):  # noqa: F811
    from dagster_and_etl.completed.lesson_6.definitions import defs

    assert defs
