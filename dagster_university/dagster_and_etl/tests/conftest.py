import pytest


@pytest.fixture(autouse=True)
def duckdb_path_env(monkeypatch):
    monkeypatch.setenv("DUCKDB_DATABASE", "data/staging/data.duckdb")


@pytest.fixture(autouse=True)
def nasa_api_key_env(monkeypatch):
    monkeypatch.setenv("NASA_API_KEY", "DEMO_KEY")
