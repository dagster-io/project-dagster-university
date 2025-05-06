import pytest


@pytest.fixture(autouse=True)
def duckdb_env_path(monkeypatch):
    monkeypatch.setenv("DUCKDB_DATABASE", "data/staging/data.duckdb")
    monkeypatch.setenv("NASA_API_KEY", "DEMO_KEY")
