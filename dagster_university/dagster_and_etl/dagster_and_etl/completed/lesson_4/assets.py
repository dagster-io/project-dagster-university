import csv
from pathlib import Path

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


class NasaDateRange(dg.Config):
    start_date: str
    end_date: str


@dg.asset
def asteroids(
    context: dg.AssetExecutionContext,
    config: NasaDateRange,
    nasa: NASAResource,
):
    return nasa.get_near_earth_asteroids(
        start_date=config.start_date,
        end_date=config.end_date,
    )


@dg.asset
def asteroids_file(
    context: dg.AssetExecutionContext,
    config: NasaDateRange,
    asteroids,
):
    filename = f"asteroid_staging_{config.start_date}_{config.end_date}"
    file_path = (
        Path(__file__).absolute().parent / f"../../../data/staging/{filename}.csv"
    )

    # Only load specific fields
    fields = [
        "id",
        "name",
        "absolute_magnitude_h",
        "is_potentially_hazardous_asteroid",
    ]

    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)

        writer.writeheader()
        for row in asteroids:
            filtered_row = {key: row[key] for key in fields if key in row}
            writer.writerow(filtered_row)

    return file_path


@dg.asset
def duckdb_table(
    context: dg.AssetExecutionContext,
    database: DuckDBResource,
    asteroids_file,
):
    table_name = "raw_asteroid_data"
    with database.get_connection() as conn:
        table_query = f"""
            create table if not exists {table_name} (
                id varchar(10),
                name varchar(100),
                absolute_magnitude_h float,
                is_potentially_hazardous_asteroid boolean
            ) 
        """
        conn.execute(table_query)
        conn.execute(f"COPY {table_name} FROM '{asteroids_file}'")
