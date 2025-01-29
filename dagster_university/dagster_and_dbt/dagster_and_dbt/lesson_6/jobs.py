from dagster import AssetSelection, define_asset_job
from dagster_dbt import build_dbt_asset_selection

from .assets.dbt import dbt_analytics
from .partitions import monthly_partition, weekly_partition

trips_by_week = AssetSelection.assets("trips_by_week")
adhoc_request = AssetSelection.assets("adhoc_request")

dbt_trips_selection = build_dbt_asset_selection([dbt_analytics], "stg_trips+")

# TODO: Fix job for different partitions
# trip_update_job = define_asset_job(
#     name="trip_update_job",
#     partitions_def=monthly_partition,
#     selection=AssetSelection.all()
#     - trips_by_week
#     - adhoc_request
#     - dbt_trips_selection,
# )

weekly_update_job = define_asset_job(
    name="weekly_update_job", partitions_def=weekly_partition, selection=trips_by_week
)

adhoc_request_job = define_asset_job(name="adhoc_request_job", selection=adhoc_request)
