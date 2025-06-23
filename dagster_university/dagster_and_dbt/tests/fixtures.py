import os
import subprocess

import pytest


def _dbt_command(cmd: str, lesson: str):
    """Run a dbt command within a specific project lesson dbt project"""
    dir = os.path.join(
        os.path.dirname(__file__),
        f"../src/dagster_and_dbt/completed/{lesson}/analytics",
    )

    cmd = ["dbt", cmd, "--project-dir", dir, "--profiles-dir", dir]
    print(cmd)
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)

    if result.returncode != 0:
        pytest.fail(f"dbt command failed: {result.returncode}")


@pytest.fixture(scope="session", autouse=True)
def setup_dbt_env(request):
    """Run necessary dbt commands to generate the dbt manifest.json required for Dagster to parse"""
    lesson_num = request.param
    _dbt_command("deps", lesson_num)
    _dbt_command("parse", lesson_num)
