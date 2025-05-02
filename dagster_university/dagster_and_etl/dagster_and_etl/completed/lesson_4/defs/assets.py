import csv
import datetime
from pathlib import Path

import dagster as dg
from dagster_duckdb import DuckDBResource

from dagster_and_etl.completed.lesson_4.defs.resources import NASAResource


class NasaDateRange(dg.Config):
    start_date: str
    end_date: str


@dg.asset(
    kinds={"nasa"},
    group_name="api_etl",
)
def asteroids(
    context: dg.AssetExecutionContext,
    config: NasaDateRange,
    nasa: NASAResource,
):
    return nasa.get_near_earth_asteroids(
        start_date=config.start_date,
        end_date=config.end_date,
    )


@dg.asset(
    group_name="api_etl",
)
def asteroids_file(
    context: dg.AssetExecutionContext,
    asteroids,
):
    filename = "asteroid_staging"
    file_path = (
        Path(__file__).absolute().parent / f"../../../../data/staging/{filename}.csv"
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


@dg.asset(
    kinds={"duckdb"},
    group_name="api_etl",
)
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


nasa_partitions_def = dg.DailyPartitionsDefinition(
    start_date="2025-04-01",
)


@dg.asset(
    kinds={"nasa"},
    group_name="api_etl",
    partitions_def=nasa_partitions_def,
)
def asteroids_partition(
    context: dg.AssetExecutionContext,
    nasa: NASAResource,
):
    anchor_date = datetime.datetime.strptime(context.partition_key, "%Y-%m-%d")
    end_date = (anchor_date - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    return nasa.get_near_earth_asteroids(
        start_date=context.partition_key,
        end_date=end_date,
    )
