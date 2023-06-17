from dagster_university.resources import get_database_resource
from dagster._core.test_utils import environ
from dagster_gcp import BigQueryResource
from dagster_duckdb import DuckDBResource

def test_get_database_resource_in_prod():
    assert isinstance(get_database_resource("prod"), BigQueryResource)

def test_get_database_resource_in_local():
    assert isinstance(get_database_resource("local"), DuckDBResource)

def test_get_database_resource_default():
    assert isinstance(get_database_resource("ajjklasjdklasjdklasdjoiwjd"), DuckDBResource)