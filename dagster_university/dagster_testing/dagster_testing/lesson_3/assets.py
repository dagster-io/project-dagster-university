import csv
import os
from typing import Iterator

import dagster as dg


@dg.asset
def state_population_file() -> list[dict]:
    current_file_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(current_file_dir, "../data/ny.csv")
    with open(file_path) as file:
        reader = csv.DictReader(file)
        return [row for row in reader]


@dg.asset
def total_population(state_population_file: list[dict]) -> int:
    return sum([int(x["Population"]) for x in state_population_file])


@dg.asset
def total_population_meta(state_population_file: list[dict]) -> dg.MaterializeResult:
    result = sum([int(x["Population"]) for x in state_population_file])
    return dg.MaterializeResult(metadata={"total_population": result})


@dg.asset
def total_population_meta_yield(state_population_file: list[dict]) -> Iterator:
    result = sum([int(x["Population"]) for x in state_population_file])
    yield dg.MaterializeResult(metadata={"total_population": result})


@dg.asset
def processed_file_meta_context(
    context: dg.AssetExecutionContext, city_population: list[dict]
) -> str:
    result = sum([int(x["Population"]) for x in city_population])
    context.log(f"File contents {result}")
    return result


def func_wrong_type() -> str:
    return 2


@dg.asset
def total_population_wrong_type(state_population_file: list[dict]) -> str:
    return sum([int(x["Population"]) for x in state_population_file])


class FilepathConfig(dg.Config):
    path: str


@dg.asset
def state_population_file_config(config: FilepathConfig) -> list[dict]:
    with open(config.path) as file:
        reader = csv.DictReader(file)
        return [row for row in reader]


@dg.asset
def total_population_config(state_population_file_config: list[dict]) -> int:
    return sum([int(x["Population"]) for x in state_population_file_config])


@dg.asset()
def state_population_file_logging(context: dg.AssetExecutionContext) -> list[dict]:
    current_file_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(current_file_dir, "../data/ny.csv")

    context.log.info(f"Reading file {file_path}")

    with open(file_path) as file:
        reader = csv.DictReader(file)
        return [row for row in reader]


file_partitions = dg.StaticPartitionsDefinition(["ca.csv", "mn.csv", "ny.csv"])


@dg.asset(partitions_def=file_partitions)
def state_population_file_partition(context: dg.AssetExecutionContext) -> list[dict]:
    current_file_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(current_file_dir, f"../data/{context.partition_key}")
    with open(file_path) as file:
        reader = csv.DictReader(file)
        return [row for row in reader]


number_partitions = dg.StaticPartitionsDefinition(["A", "B", "C"])


@dg.asset(partitions_def=number_partitions)
def partition_asset_letter(context: dg.AssetExecutionContext) -> str:
    return context.partition_key
