import os
import subprocess

import pytest


def _dbt_command(cmd: str, lesson: str):
    dir = os.path.join(os.path.dirname(__file__), f"../dagster_and_dbt/{lesson}/analytics")

    cmd = ["dbt", cmd, "--project-dir", dir, "--profiles-dir", dir]
    print(cmd)
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)

    if result.returncode != 0:
        pytest.fail(f"dbt command failed: {result.returncode}")


@pytest.fixture(scope="session", autouse=True)
def setup_dbt_env(request):
    """Run necessary dbt commands to generate the dbt target/manifest in the dbt project"""
    lesson_num = request.param
    _dbt_command("deps", lesson_num)
    _dbt_command("parse", lesson_num)