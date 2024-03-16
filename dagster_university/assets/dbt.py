from dagster import AssetExecutionContext
from dagster_dbt import dbt_assets, DbtCliResource

import os

from .constants import DBT_DIRECTORY

dbt_manifest_path = os.path.join(DBT_DIRECTORY, "target", "manifest.json")

@dbt_assets(
    manifest=dbt_manifest_path,
)
def dbt_analytics(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["run"], context=context).stream()
