# TODO: Resolve that annoying relative import error to get the test to actually run

from ..dagster_university.resources import get_database_resource
from dagster._core.test_utils import environ
from dagster_gcp import BigQueryResource
from dagster_duckdb import DuckDBResource

def test_get_database_resource_in_prod():
    with environ({
            "DAGSTER_ENVIRONMENT": "prod",
    }):
        assert isinstance(get_database_resource(), BigQueryResource)

def test_get_database_resource_in_local():
    with environ({
            "DAGSTER_ENVIRONMENT": "local",
    }):
        assert isinstance(get_database_resource(), DuckDBResource)

def test_get_database_resource_default():
    with environ({
            "DAGSTER_ENVIRONMENT": "ajjklasjdklasjdklasdjoiwjd",
    }):
        assert isinstance(get_database_resource(), DuckDBResource)