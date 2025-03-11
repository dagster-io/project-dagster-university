from pathlib import Path

import dagster as dg
import yaml

import dagster_testing.assets.dagster_assets as dagster_assets

my_job = dg.define_asset_job(
    name="jobs",
    selection=[
        dagster_assets.population_file_config,
        dagster_assets.population_api_resource,
        dagster_assets.population_combined,
    ],
)


my_job_configured = dg.define_asset_job(
    name="jobs_config",
    selection=[
        dagster_assets.population_file_config,
        dagster_assets.population_api_resource,
        dagster_assets.population_combined,
    ],
    config=yaml.safe_load(
        (Path(__file__).absolute().parent / "configs/run_config.yaml").open()
    ),
)
