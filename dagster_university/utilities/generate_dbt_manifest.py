from dbt.cli.main import dbtRunner
from dbt.contracts.graph.manifest import Manifest

import os
import sys

def generate_dbt_manifest(dbt_project_dir, manifest_path):
    manifest_file_path = os.path.join(manifest_path, "manifest.json")
    
    print(f"Building manifest.json for dbt project at {dbt_project_dir}")

    res = dbtRunner().invoke([
        "parse",
        "--project-dir",
        dbt_project_dir,
        "--profiles-dir",
        dbt_project_dir,
        "--target",
        "dagster"
    ])

    manifest: Manifest = res.result # type: ignore

    print(f"Writing manifest.json to {manifest_file_path}")

    manifest.write(manifest_file_path)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise ValueError("Must provide path to dbt project and output path") 

    path_to_dbt_project = sys.argv[1]
    output_path = sys.argv[2]

    generate_dbt_manifest(path_to_dbt_project, output_path)