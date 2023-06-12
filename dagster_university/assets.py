from dagster import asset

@asset
def test_asset():
    return 1