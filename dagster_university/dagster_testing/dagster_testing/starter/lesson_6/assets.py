import csv
from pathlib import Path

import dagster as dg

import dagster_testing.starter.lesson_6.resources as resources


class FilepathConfig(dg.Config):
    path: str


@dg.asset
def state_population_file_config(config: FilepathConfig) -> list[dict]:
    with open(config.path) as file:
        reader = csv.DictReader(file)
        return [row for row in reader]


@dg.asset
def state_population_api_resource(
    state_population_resource: resources.StatePopulation,
) -> list[dict]:
    return state_population_resource.get_cities("wi")


@dg.asset
def total_population(
    state_population_file_config: list[dict],
    state_population_api_resource: list[dict],
) -> int:
    all_assets = state_population_file_config + state_population_api_resource
    return sum([int(x["Population"]) for x in all_assets])


@dg.asset_check(asset=total_population)
def non_negative(total_population):
    return dg.AssetCheckResult(
        passed=bool(total_population > 0),
    )


file_partitions = dg.StaticPartitionsDefinition(["ca.csv", "mn.csv", "ny.csv"])


@dg.asset(partitions_def=file_partitions)
def state_population_file_partition(context: dg.AssetExecutionContext) -> list[dict]:
    file_path = (
        Path(__file__).absolute().parent / f"../../data/{context.partition_key}.csv"
    )
    with open(file_path) as file:
        reader = csv.DictReader(file)
        return [row for row in reader]


@dg.asset
def total_population_partition(state_population_file_partition: list[dict]) -> int:
    return sum([int(x["Population"]) for x in state_population_file_partition])
