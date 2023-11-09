from dagster import AssetKey, AssetExecutionContext
from dagster_dbt.asset_decorator import dbt_assets
from ..resources import DBT_MANIFEST_PATH, dbt_resource

# manifest_path = "data/staging/manifest.json"
# dbt_project_dir = "transformations"

# class TransformationsManifest(DbtManifest):

#     @classmethod
#     def node_info_to_asset_key(cls, node_info):
#         # Prefix the asset key with `taxi_` because the tables made by in `trips.py` don't have a prefix
#         if node_info["resource_type"] == "source":
#             return AssetKey([f"taxi_{node_info['identifier']}"])
        
#         return super().node_info_to_asset_key(node_info)

@dbt_assets(
    manifest=DBT_MANIFEST_PATH,
)
def transformation_dbt_assets(context: AssetExecutionContext):
    dbt_resource.cli(["seed"], context=context).wait()
    yield from dbt_resource.cli(["build"], context=context).stream()