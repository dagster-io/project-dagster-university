from dagster import define_asset_job, AssetSelection
from dagster_dbt import build_dbt_asset_selection

from ..assets.dbt import analytics_project
from ..partitions import monthly_partition, weekly_partition

trips_by_week = AssetSelection.keys("trips_by_week")
adhoc_request = AssetSelection.keys("adhoc_request")

trip_update_job = define_asset_job(
    name="trip_update_job",
    partitions_def=monthly_partition,
    selection=AssetSelection.all() - trips_by_week - adhoc_request - build_dbt_asset_selection([analytics_project], "daily_metrics")
)

weekly_update_job = define_asset_job(
    name="weekly_update_job",
    partitions_def=weekly_partition,
    selection=trips_by_week
)

adhoc_request_job = define_asset_job(
    name="adhoc_request_job",
    selection=adhoc_request
)