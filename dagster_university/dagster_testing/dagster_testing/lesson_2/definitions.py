import dagster as dg

from .assets import (
    loaded_file,
    loaded_file_config,
    processed_file,
    processed_file_config,
    wrong_type_annotation,
)

defs = dg.Definitions(
    assets=[
        loaded_file,
        processed_file,
        wrong_type_annotation,
        loaded_file_config,
        processed_file_config,
    ],
)
