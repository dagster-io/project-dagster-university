import dagster as dg
import requests
from dagster_duckdb import DuckDBResource


class NASAResource(dg.ConfigurableResource):
    api_key: str

    def get_near_earth_asteroids(self, start_date: str, end_date: str):
        url = "https://api.nasa.gov/neo/rest/v1/feed"
        params = {
            "start_date": start_date,
            "end_date": end_date,
            "api_key": self.api_key,
        }

        resp = requests.get(url, params=params)
        return resp.json()["near_earth_objects"][start_date]


defs = dg.Definitions(
    resources={
        "nasa": NASAResource(
            api_key=dg.EnvVar("NASA_API_KEY"),
        ),
        "database": DuckDBResource(
            database="data/staging/data.duckdb",
        ),
    },
)
