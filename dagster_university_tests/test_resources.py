from dagster_university.resources import get_database_resource

from dagster_duckdb import DuckDBResource

from dagster_university.resources.postgres import PostgresResource

def test_get_database_resource_in_prod():
    assert isinstance(get_database_resource("prod"), PostgresResource)

def test_get_database_resource_in_local():
    assert isinstance(get_database_resource("local"), DuckDBResource)

def test_get_database_resource_default():
    assert isinstance(get_database_resource("ajjklasjdklasjdklasdjoiwjd"), DuckDBResource)