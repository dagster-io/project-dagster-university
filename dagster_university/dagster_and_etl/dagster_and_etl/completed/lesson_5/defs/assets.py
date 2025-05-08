import csv
import datetime
import os
from pathlib import Path

import dagster as dg
import dlt
import requests
from dagster_dlt import DagsterDltResource, DagsterDltTranslator, dlt_assets
from dagster_dlt.translator import DltResourceTranslatorData


@dlt.source
def simple_source():
    @dlt.resource
    def load_dict():
        data = [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"},
        ]

        yield data

    return load_dict


# TODO: Enable multiple dlt assets
# @dlt_assets(
#     dlt_source=simple_source(),
#     dlt_pipeline=dlt.pipeline(
#         pipeline_name="simple_pipeline",
#         dataset_name="simple",
#         destination="duckdb",
#         progress="log",
#     ),
# )
# def dlt_assets(context: dg.AssetExecutionContext, dlt: DagsterDltResource):
#     yield from dlt.run(context=context)


class FilePath(dg.Config):
    path: str


@dg.asset
def import_file(context: dg.AssetExecutionContext, config: FilePath) -> str:
    file_path = (
        Path(__file__).absolute().parent / f"../../../../data/source/{config.path}"
    )
    return str(file_path.resolve())


@dlt.source
def csv_source(file_path: str = None):
    def load_csv():
        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            data = [row for row in reader]

        yield data

    return load_csv


class CustomDagsterDltTranslator(DagsterDltTranslator):
    def get_asset_spec(self, data: DltResourceTranslatorData) -> dg.AssetSpec:
        default_spec = super().get_asset_spec(data)
        return default_spec.replace_attributes(
            deps=[dg.AssetKey("import_file")],
        )


@dlt_assets(
    dlt_source=csv_source(),
    dlt_pipeline=dlt.pipeline(
        pipeline_name="csv_pipeline",
        dataset_name="csv_data",
        destination="duckdb",
        progress="log",
    ),
    dagster_dlt_translator=CustomDagsterDltTranslator(),
)
def dlt_csv_assets(
    context: dg.AssetExecutionContext, dlt: DagsterDltResource, import_file
):
    yield from dlt.run(context=context, dlt_source=csv_source(import_file))


class NasaDate(dg.Config):
    date: str


@dg.asset
def dlt_nasa(context: dg.AssetExecutionContext, config: NasaDate):
    anchor_date = datetime.datetime.strptime(config.date, "%Y-%m-%d")
    start_date = (anchor_date - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    @dlt.source
    def nasa_neo_source():
        @dlt.resource
        def load_neo_data():
            url = "https://api.nasa.gov/neo/rest/v1/feed"
            params = {
                "start_date": start_date,
                "end_date": config.date,
                "api_key": os.getenv("NASA_API_KEY"),
            }

            response = requests.get(url, params=params)
            response.raise_for_status()

            data = response.json()

            for neo in data["near_earth_objects"][config.date]:
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


nasa_partitions_def = dg.DailyPartitionsDefinition(
    start_date="2015-09-01",
)


@dg.asset(
    partitions_def=nasa_partitions_def,
)
def dlt_nasa_partition(context: dg.AssetExecutionContext):
    anchor_date = datetime.datetime.strptime(context.partition_key, "%Y-%m-%d")
    start_date = (anchor_date - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    @dlt.source
    def nasa_neo_source():
        @dlt.resource
        def load_neo_data():
            url = "https://api.nasa.gov/neo/rest/v1/feed"
            params = {
                "start_date": start_date,
                "end_date": context.partition_key,
                "api_key": os.getenv("NASA_API_KEY"),
            }

            response = requests.get(url, params=params)
            response.raise_for_status()

            data = response.json()

            for neo in data["near_earth_objects"][context.partition_key]:
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
