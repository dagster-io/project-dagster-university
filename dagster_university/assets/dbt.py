from dagster import AssetKey, AssetExecutionContext, Config, BackfillPolicy
from dagster_dbt import dbt_assets, DbtCliResource, DagsterDbtTranslator

from pathlib import Path

import os
import json

from .constants import DBT_DIRECTORY
from ..resources import dbt_resource
from ..partitions import daily_partition

class DbtConfig(Config):
    full_refresh: bool = False

class CustomizedDagsterDbtTranslator(DagsterDbtTranslator):

    @classmethod
    def get_asset_key(cls, dbt_resource_props):
        if dbt_resource_props["resource_type"] == "source":
            return AssetKey(f"taxi_{dbt_resource_props['name']}")
        else:
            return AssetKey(dbt_resource_props["name"])
        
    @classmethod
    def get_metadata(cls, dbt_node_info):
        return {
            "columns": dbt_node_info["columns"],
            "sources": dbt_node_info["sources"],
            "description": dbt_node_info["description"],
        }
        
if os.getenv("DAGSTER_DBT_PARSE_PROJECT_ON_LOAD"):
    dbt_manifest_path = (
        dbt_resource.cli(
            ["--quiet", "parse"],
            target_path=Path("target"),
        )
        .wait()
        .target_path.joinpath("manifest.json")
    )
else:
    dbt_manifest_path = DBT_DIRECTORY.joinpath("target", "manifest.json")

@dbt_assets(
    manifest=dbt_manifest_path,
    dagster_dbt_translator=CustomizedDagsterDbtTranslator(),
    exclude="config.materialized:incremental",
)
def analytics_project(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["run"], context=context).stream()


@dbt_assets(
    manifest=dbt_manifest_path,
    dagster_dbt_translator=CustomizedDagsterDbtTranslator(),
    select="config.materialized:incremental",
    partitions_def=daily_partition,
    backfill_policy=BackfillPolicy.single_run()
)
def incremental_dbt_models(
    context: AssetExecutionContext,
    dbt: DbtCliResource,
    config: DbtConfig
):
    time_window = context.asset_partitions_time_window_for_output(
        next(iter(context.selected_output_names))
    )

    dbt_vars = {
        "min_date": time_window.start.isoformat(),
        "max_date": time_window.end.isoformat()
    }
    args = (
        ["build", "--full-refresh"]
        if config.full_refresh
        else ["build", "--vars", json.dumps(dbt_vars)]
    )
    yield from dbt.cli(args, context=context).stream()