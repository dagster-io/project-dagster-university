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


@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    monkeypatch.setenv("DUCKDB_DATABASE", "data/staging/data.duckdb")


def pytest_configure(config):
    print("Setting dbt env manifest")

    for lesson_n in ["lesson_3", "lesson_4", "lesson_5", "lesson_6", "lesson_7"]:
        _dbt_command("deps", lesson_n)
        _dbt_command("parse", lesson_n)
