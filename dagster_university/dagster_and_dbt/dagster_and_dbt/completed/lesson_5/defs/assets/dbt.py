import dagster as dg
from dagster_dbt import DagsterDbtTranslator, DbtCliResource, dbt_assets

from dagster_and_dbt.completed.lesson_5.defs.project import dbt_project


class CustomizedDagsterDbtTranslator(DagsterDbtTranslator):
    # SCREENSHOT: Comment out screenshots before "Group dbt models"
    def get_group_name(self, dbt_resource_props):
        return dbt_resource_props["fqn"][1]

    def get_asset_key(self, dbt_resource_props):
        resource_type = dbt_resource_props["resource_type"]
        name = dbt_resource_props["name"]
        if resource_type == "source":
            return dg.AssetKey(f"taxi_{name}")
        else:
            return super().get_asset_key(dbt_resource_props)


@dbt_assets(
    manifest=dbt_project.manifest_path,
    dagster_dbt_translator=CustomizedDagsterDbtTranslator(),
)
def dbt_analytics(context: dg.AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["run"], context=context).stream()
