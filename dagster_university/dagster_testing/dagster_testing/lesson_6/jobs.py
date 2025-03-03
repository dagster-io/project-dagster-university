from pathlib import Path

import dagster as dg
import yaml

state_population_file_partition = dg.AssetSelection.assets(
    "state_population_file_partition"
)
total_population_partition = dg.AssetSelection.assets("total_population_partition")


my_job = dg.define_asset_job(
    name="jobs",
    selection=dg.AssetSelection.all()
    - state_population_file_partition
    - total_population_partition,
)


my_job_configured = dg.define_asset_job(
    name="jobs_config",
    selection=dg.AssetSelection.all()
    - state_population_file_partition
    - total_population_partition,
    config=yaml.safe_load(
        (Path(__file__).absolute().parent / "run_config.yaml").open()
    ),
)
