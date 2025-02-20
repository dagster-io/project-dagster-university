import os
from typing import Iterator

import dagster as dg


@dg.asset
def loaded_file() -> str:
    current_file_path = os.path.dirname(os.path.realpath(__file__))
    file_name = os.path.join(current_file_path, "path.txt")
    with open(file_name) as file:
        return file.read()


@dg.asset
def processed_file(loaded_file: str) -> str:
    return loaded_file.strip()


@dg.asset
def processed_file_meta(loaded_file: str) -> dg.MaterializeResult:
    result = loaded_file.strip()
    return dg.MaterializeResult(metadata={"file_content": result})


@dg.asset
def processed_file_meta_yield(loaded_file: str) -> Iterator:
    result = loaded_file.strip()
    yield dg.MaterializeResult(metadata={"file_content": result})


@dg.asset
def processed_file_meta_context(
    context: dg.AssetExecutionContext, loaded_file: str
) -> str:
    result = loaded_file.strip()
    context.log(f"File contents {result}")
    return result


def func_wrong_type() -> str:
    return 2


@dg.asset
def wrong_type_annotation() -> str:
    return 2


class FilepathConfig(dg.Config):
    path: str


@dg.asset
def loaded_file_config(config: FilepathConfig) -> str:
    current_file_path = os.path.dirname(os.path.realpath(__file__))
    file_name = os.path.join(current_file_path, config.path)
    with open(file_name) as file:
        return file.read()


@dg.asset
def processed_file_config(loaded_file_config: str) -> str:
    return loaded_file_config.strip()


@dg.asset()
def loaded_file_logging(context: dg.AssetExecutionContext) -> str:
    current_file_path = os.path.dirname(os.path.realpath(__file__))
    file_name = os.path.join(current_file_path, "path.txt")

    context.log.info(f"Reading file {file_name}")

    with open(file_name) as file:
        return file.read()


number_partitions = dg.StaticPartitionsDefinition(["1", "2", "3"])


@dg.asset(partitions_def=number_partitions)
def partition_asset_number(context: dg.AssetExecutionContext) -> int:
    return int(context.partition_key)


number_partitions = dg.StaticPartitionsDefinition(["A", "B", "C"])


@dg.asset(partitions_def=number_partitions)
def partition_asset_letter(context: dg.AssetExecutionContext) -> str:
    return context.partition_key
