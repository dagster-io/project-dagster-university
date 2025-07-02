import dagster as dg
import pytest

from tests.fixtures import docker_compose  # noqa: F401

# @pytest.mark.integration
# def test_postgres_component_sling_assets(docker_compose):  # noqa: F811
#     from dagster_and_etl.completed.lesson_7.definitions import defs

#     result = dg.materialize(assets=[asset for asset in defs.assets])
#     assert result.success


# @pytest.mark.integration
# def test_component_asset_metadata(docker_compose):  # noqa: F811
#     from dagster_and_etl.completed.lesson_7.definitions import defs

#     # Get all component assets
#     component_assets = [
#         asset for asset in defs.assets if hasattr(asset, "component_name")
#     ]

#     # Verify each component asset has required metadata
#     for asset in component_assets:
#         assert hasattr(asset, "component_name")
#         assert hasattr(asset, "group_name")
#         assert asset.group_name is not None
