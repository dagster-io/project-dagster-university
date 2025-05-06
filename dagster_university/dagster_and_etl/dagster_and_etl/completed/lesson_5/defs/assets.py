import csv
import os
from pathlib import Path

import dagster as dg
import dlt
import requests


@dg.asset
def dlt_simple(context: dg.AssetExecutionContext):
    data = [
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"},
    ]

    @dlt.source
    def simple_source():
        @dlt.resource
        def load_dict():
            yield data

        return load_dict

    pipeline = dlt.pipeline(
        pipeline_name="simple_pipeline",
        destination="duckdb",
        dataset_name="simple_data",
    )

    load_info = pipeline.run(simple_source())

    return load_info


class FilePath(dg.Config):
    path: str


@dg.asset
def import_file(context: dg.AssetExecutionContext, config: FilePath) -> str:
    file_path = (
        Path(__file__).absolute().parent / f"../../../../data/source/{config.path}"
    )
    return str(file_path.resolve())


@dg.asset
def dlt_load_csv(context: dg.AssetExecutionContext, import_file: str):
    with open(import_file, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]

    @dlt.source
    def csv_source():
        @dlt.resource
        def load_csv():
            yield data

        return load_csv

    pipeline = dlt.pipeline(
        pipeline_name="csv_pipeline",
        destination=dlt.destinations.duckdb(os.getenv("DUCKDB_DATABASE")),
        dataset_name="csv_data",
    )

    load_info = pipeline.run(csv_source())

    return load_info


class NasaDateRange(dg.Config):
    start_date: str
    end_date: str


@dg.asset
def dlt_nasa(context: dg.AssetExecutionContext, config: NasaDateRange):
    @dlt.source
    def nasa_neo_source():
        @dlt.resource
        def load_neo_data():
            url = "https://api.nasa.gov/neo/rest/v1/feed"
            params = {
                "start_date": config.start_date,
                "end_date": config.end_date,
                "api_key": os.getenv("NASA_API_KEY"),
            }

            response = requests.get(url, params=params)
            response.raise_for_status()

            data = response.json()

            for neo in data["near_earth_objects"][config.start_date]:
                neo_data = {
                    "id": neo["id"],
                    "name": neo["name"],
                    "absolute_magnitude_h": neo["absolute_magnitude_h"],
                    "is_potentially_hazardous": neo[
                        "is_potentially_hazardous_asteroid"
                    ],
                }

                yield neo_data

        return load_neo_data

    pipeline = dlt.pipeline(
        pipeline_name="nasa_neo_pipeline",
        destination=dlt.destinations.duckdb(os.getenv("DUCKDB_DATABASE")),
        dataset_name="nasa_neo",
    )

    load_info = pipeline.run(nasa_neo_source())

    return load_info
