from pathlib import Path

import dagster as dg
import yaml

my_job = dg.define_asset_job(
    name="jobs",
    selection=dg.AssetSelection.all(),
)


my_job_configured = dg.define_asset_job(
    name="jobs_config",
    selection=dg.AssetSelection.all(),
    config=yaml.safe_load(
        (Path(__file__).absolute().parent / "run_config.yaml").open()
    ),
)
