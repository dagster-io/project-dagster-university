import tempfile
from pathlib import Path

import dagster as dg
import pytest
from dagster_duckdb import DuckDBResource

from ai_driven_data_engineering.definitions import defs as defs_fn


@pytest.fixture
def defs():
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
