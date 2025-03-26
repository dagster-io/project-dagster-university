from pathlib import Path

import dagster as dg
import yaml

from dagster_testing.assets import lesson_6

my_job = dg.define_asset_job(
    name="jobs",
    selection=[
        lesson_6.population_file_config,
        lesson_6.population_api_resource,
        lesson_6.population_combined,
    ],
)


my_job_configured = dg.define_asset_job(
    name="jobs_config",
    selection=[
        lesson_6.population_file_config,
        lesson_6.population_api_resource,
        lesson_6.population_combined,
    ],
    config=yaml.safe_load(
        (Path(__file__).absolute().parent / "configs/run_config.yaml").open()
    ),
)
