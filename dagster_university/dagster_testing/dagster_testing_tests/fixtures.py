import subprocess
import time
from pathlib import Path

import pytest


@pytest.fixture(scope="session", autouse=True)
def docker_compose():
    # Start Docker Compose
    file_path = Path(__file__).absolute().parent / "docker-compose.yaml"
    subprocess.run(["docker-compose", "-f", file_path, "up", "-d"], check=True)

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
    subprocess.run(["docker-compose", "-f", file_path, "down"], check=True)
