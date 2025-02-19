from datetime import datetime

import dagster as dg

import dagster_testing.lesson_5.resources as resources


@dg.daily_partitioned_config(start_date=datetime(2020, 1, 1))
def my_partitioned_config(start: datetime, _end: datetime):
    return {
        "ops": {
            "process_data_for_date": {"config": {"date": start.strftime("%Y-%m-%d")}}
        }
    }


class AssetConfig(dg.Config):
    number: int


@dg.asset
def config_asset(config: AssetConfig) -> int:
    return config.number


@dg.asset
def resource_asset(number: resources.ExampleResource) -> int:
    return number.number_5()


number_partitions = dg.StaticPartitionsDefinition(["1", "2", "3"])


@dg.asset(partitions_def=number_partitions)
def partition_asset(context: dg.AssetExecutionContext) -> int:
    return int(context.partition_key)


@dg.asset
def combine_asset(config_asset: int, resource_asset: int, partition_asset: int) -> int:
    return config_asset + resource_asset + partition_asset


@dg.asset_check(asset=combine_asset)
def non_negative(combine_asset):
    return dg.AssetCheckResult(
        passed=bool(combine_asset > 0),
    )


@dg.asset
def final_asset(combine_asset: int) -> int:
    return combine_asset * 10
