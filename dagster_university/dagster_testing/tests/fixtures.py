import subprocess
import time
from pathlib import Path

import pytest


@pytest.fixture(scope="session", autouse=True)
def docker_compose():
    file_path = Path(__file__).absolute().parent / "docker-compose.yaml"

    # Tear down any existing containers and volumes to ensure clean state
    subprocess.run(
        ["docker", "compose", "-f", file_path, "down", "-v"],
        capture_output=True,
    )

    # Start Docker Compose
    subprocess.run(
        ["docker", "compose", "-f", file_path, "up", "--build", "-d"],
        check=True,
        capture_output=True,
    )

    # Wait for PostgreSQL to be ready to accept connections
    max_retries = 10
    for i in range(max_retries):
        result = subprocess.run(
            ["docker", "exec", "postgresql", "pg_isready"],
            capture_output=True,
        )
        if result.returncode == 0:
            break
        time.sleep(2)

    # Wait for the initialization scripts to complete (schema and table creation)
    for i in range(max_retries):
        result = subprocess.run(
            [
                "docker",
                "exec",
                "postgresql",
                "psql",
                "-U",
                "test_user",
                "-d",
                "test_db",
                "-c",
                "SELECT 1 FROM data.city_population LIMIT 1;",
            ],
            capture_output=True,
        )
        if result.returncode == 0:
            break
        time.sleep(2)

    yield

    # Tear down Docker Compose and remove volumes
    subprocess.run(["docker", "compose", "-f", file_path, "down", "-v"], check=True)
