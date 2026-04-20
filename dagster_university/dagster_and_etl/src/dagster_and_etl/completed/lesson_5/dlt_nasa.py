import os

import dlt
import requests


@dlt.source
def nasa_neo_source(start_date: str, end_date: str, api_key: str):
    @dlt.resource
    def fetch_neo_data():
        url = "https://api.nasa.gov/neo/rest/v1/feed"
        params = {
            "start_date": start_date,
            "end_date": end_date,
            "api_key": api_key,
        }

        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()

        for neo in data["near_earth_objects"][start_date]:
            neo_data = {
                "id": neo["id"],
                "name": neo["name"],
                "absolute_magnitude_h": neo["absolute_magnitude_h"],
                "is_potentially_hazardous": neo["is_potentially_hazardous_asteroid"],
            }

            yield neo_data

    return fetch_neo_data


pipeline = dlt.pipeline(
    pipeline_name="nasa_neo_pipeline",
    destination=dlt.destinations.duckdb(os.getenv("DUCKDB_DATABASE")),
    dataset_name="nasa_neo",
)

if __name__ == "__main__":
    # Use merge with primary_key to handle re-runs without creating duplicates
    load_info = pipeline.run(
        nasa_neo_source(
            start_date="2015-09-07",
            end_date="2015-09-08",
            api_key="DEMO_KEY",
        ),
        write_disposition="merge",
        primary_key="id",
    )
