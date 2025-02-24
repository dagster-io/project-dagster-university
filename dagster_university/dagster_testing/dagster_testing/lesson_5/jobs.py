from pathlib import Path

import dagster as dg
import yaml

partition_asset = dg.AssetSelection.assets("partition_asset")

my_job = dg.define_asset_job(
    name="jobs",
    selection=dg.AssetSelection.all() - partition_asset,
)


my_job_configured = dg.define_asset_job(
    name="jobs_config",
    selection=dg.AssetSelection.all() - partition_asset,
    config=yaml.safe_load(
        (Path(__file__).absolute().parent / "run_config.yaml").open()
    ),
)
