from dagster import AssetKey, AssetExecutionContext
from dagster_dbt import dbt_assets, DbtCliResource, DagsterDbtTranslator
from pathlib import Path

import os
import json

from .constants import DBT_DIRECTORY
from ..resources import dbt_resource
from ..partitions import daily_partition

class CustomizedDagsterDbtTranslator(DagsterDbtTranslator):

    @classmethod
    def get_asset_key(cls, dbt_resource_props):
        type = dbt_resource_props["resource_type"]
        name = dbt_resource_props["name"]
        if type == "source":
            return AssetKey(f"taxi_{name}")
        else:
            return super().get_asset_key(dbt_resource_props)
        
    @classmethod
    def get_metadata(cls, dbt_node_info):
        return {
            "columns": dbt_node_info["columns"],
            "sources": dbt_node_info["sources"],
            "description": dbt_node_info["description"],
        }

    @classmethod
    def get_group_name(cls, dbt_resource_props):
        return dbt_resource_props["fqn"][1]
        
if os.getenv("DAGSTER_DBT_PARSE_PROJECT_ON_LOAD"):
    dbt_manifest_path = (
        dbt_resource.cli(
            ["--quiet", "parse"],
            target_path=Path("target")
        )
        .wait()
        .target_path.joinpath("manifest.json")
    )
else:
    dbt_manifest_path = os.path.join(DBT_DIRECTORY, "target", "manifest.json")

INCREMENTAL_SELECTOR = "config.materialized:incremental"

@dbt_assets(
    manifest=dbt_manifest_path,
    dagster_dbt_translator=CustomizedDagsterDbtTranslator(),
    exclude=INCREMENTAL_SELECTOR,
)
def dbt_analytics(context: AssetExecutionContext, dbt: DbtCliResource):
    dbt_build_invocation = dbt.cli(["build"], context=context)

    yield from dbt_build_invocation.stream()

    run_results_json = dbt_build_invocation.get_artifact("run_results.json")
    for result in run_results_json["results"]:
        context.log.debug(result["compiled_code"])


@dbt_assets(
    manifest=dbt_manifest_path,
    dagster_dbt_translator=CustomizedDagsterDbtTranslator(),
    select=INCREMENTAL_SELECTOR,
    partitions_def=daily_partition,
)
def incremental_dbt_models(
    context: AssetExecutionContext,
    dbt: DbtCliResource
):
    time_window = context.partition_time_window

    dbt_vars = {
        "min_date": time_window.start.isoformat(),
        "max_date": time_window.end.isoformat()
    }
    
    yield from dbt.cli(["build", "--vars", json.dumps(dbt_vars)], context=context).stream()
