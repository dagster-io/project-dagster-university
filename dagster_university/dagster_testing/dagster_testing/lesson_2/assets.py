import os

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
