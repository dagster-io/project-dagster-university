from dagster import AssetKey, OpExecutionContext
from dagster_dbt.asset_decorator import dbt_assets
from dagster_dbt.cli import DbtCli, DbtManifest

manifest_path = "data/staging/manifest.json"
dbt_project_dir = "transformations"

class TransformationsManifest(DbtManifest):

    @classmethod
    def node_info_to_asset_key(cls, node_info):
        # Prefix the asset key with `taxi_` because the tables made by in `trips.py` don't have a prefix
        if node_info["resource_type"] == "source":
            return AssetKey([f"taxi_{node_info['identifier']}"])
        
        return super().node_info_to_asset_key(node_info)

manifest = TransformationsManifest.read(manifest_path)

@dbt_assets(manifest=manifest)
def transformations(context: OpExecutionContext, dbt: DbtCli):
    yield from dbt.cli(["build"], manifest=manifest, context=context).stream()