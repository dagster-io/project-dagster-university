import dagster as dg
from dagster_dbt import build_dbt_asset_selection

from dagster_and_dbt.completed.lesson_7.assets.dbt import dbt_analytics
from dagster_and_dbt.completed.lesson_7.partitions import weekly_partition

trips_by_week = dg.AssetSelection.assets("trips_by_week")
adhoc_request = dg.AssetSelection.assets("adhoc_request")

dbt_trips_selection = build_dbt_asset_selection([dbt_analytics], "stg_trips+")

# TODO: Fix job for different partitions
# trip_update_job = dg.define_asset_job(
#     name="trip_update_job",
#     partitions_def=monthly_partition,
#     selection=dg.AssetSelection.all()
#     - trips_by_week
#     - adhoc_request
#     - dbt_trips_selection,
# )

weekly_update_job = dg.define_asset_job(
    name="weekly_update_job", partitions_def=weekly_partition, selection=trips_by_week
)

adhoc_request_job = dg.define_asset_job(
    name="adhoc_request_job", selection=adhoc_request
)
