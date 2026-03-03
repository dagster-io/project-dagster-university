import subprocess
import tempfile
from pathlib import Path

import dagster as dg
import pytest
from dagster_duckdb import DuckDBResource

from ai_driven_data_engineering.definitions import defs as defs_fn

_DBT_PROJECT_DIR = Path(__file__).parent.parent / "dbt_project"


@pytest.fixture(scope="session", autouse=True)
def setup_dbt_env():
    """Run dbt parse to generate manifest.json before any tests load definitions."""
    result = subprocess.run(
        [
            "dbt",
            "parse",
            "--project-dir",
            str(_DBT_PROJECT_DIR),
            "--profiles-dir",
            str(_DBT_PROJECT_DIR),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        pytest.fail(f"dbt parse failed:\n{result.stdout}\n{result.stderr}")


@pytest.fixture
def defs(setup_dbt_env):
    """Load Definitions from the defs folder (project root)."""
    return defs_fn()


@pytest.fixture
def temp_duckdb_path():
    """Temporary DuckDB path for tests that materialize raw assets."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield str(Path(tmpdir) / "test.duckdb")


@pytest.fixture
def duckdb_resource(temp_duckdb_path):
    """DuckDB resource pointing at a temporary database."""
    return DuckDBResource(database=temp_duckdb_path)
