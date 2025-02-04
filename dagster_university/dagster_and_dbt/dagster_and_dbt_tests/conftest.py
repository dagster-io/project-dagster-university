import pytest


@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    monkeypatch.setenv("DUCKDB_DATABASE", "data/staging/data.duckdb")
