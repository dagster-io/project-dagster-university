import subprocess
import time
from pathlib import Path

import pytest
from dagster_duckdb import DuckDBResource

nasa_response = [
    {
        "links": {"self": "http://api.nasa.gov/neo/rest/v1/neo/2004034?api_key=XXX"},
        "id": "2004034",
        "neo_reference_id": "2004034",
        "name": "4034 Vishnu (1986 PA)",
        "nasa_jpl_url": "https://ssd.jpl.nasa.gov/tools/sbdb_lookup.html#/?sstr=2004034",
        "absolute_magnitude_h": 18.49,
        "estimated_diameter": {
            "kilometers": {
                "estimated_diameter_min": 0.5327886649,
                "estimated_diameter_max": 1.1913516723,
            },
            "meters": {
                "estimated_diameter_min": 532.7886648737,
                "estimated_diameter_max": 1191.3516722989,
            },
            "miles": {
                "estimated_diameter_min": 0.3310594255,
                "estimated_diameter_max": 0.74027138,
            },
            "feet": {
                "estimated_diameter_min": 1747.9943632641,
                "estimated_diameter_max": 3908.634220545,
            },
        },
        "is_potentially_hazardous_asteroid": True,
        "close_approach_data": [
            {
                "close_approach_date": "2025-04-01",
                "close_approach_date_full": "2025-Apr-01 10:03",
                "epoch_date_close_approach": 1743501780000,
                "relative_velocity": {
                    "kilometers_per_second": "11.9802215702",
                    "kilometers_per_hour": "43128.797652765",
                    "miles_per_hour": "26798.5576304083",
                },
                "miss_distance": {
                    "astronomical": "0.1567576329",
                    "lunar": "60.9787191981",
                    "kilometers": "23450607.988081923",
                    "miles": "14571532.1128716174",
                },
                "orbiting_body": "Earth",
            }
        ],
        "is_sentry_object": False,
    },
]


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
