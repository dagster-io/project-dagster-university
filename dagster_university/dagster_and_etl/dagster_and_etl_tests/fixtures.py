import subprocess
import time
from pathlib import Path

import pytest
from dagster_duckdb import DuckDBResource


@pytest.fixture()
def duckdb_resource():
    file_path = "../data/staging/data.duckdb"
    return DuckDBResource(database=file_path)


@pytest.fixture(scope="session", autouse=True)
def docker_compose():
    # Start Docker Compose
    file_path = Path(__file__).absolute().parent / "docker-compose.yaml"
    subprocess.run(
        ["docker", "compose", "-f", file_path, "up", "--build", "-d"],
        check=True,
        capture_output=True,
    )

    max_retries = 5
    for i in range(max_retries):
        result = subprocess.run(
            ["docker", "exec", "postgresql", "pg_isready"],
            capture_output=True,
        )
        if result.returncode == 0:
            break
        time.sleep(5)

    yield

    # Tear down Docker Compose
    subprocess.run(["docker", "compose", "-f", file_path, "down"], check=True)
