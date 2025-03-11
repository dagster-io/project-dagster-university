import os

import dagster as dg
import duckdb
import requests
from dagster._utils.backoff import backoff

from . import constants


@dg.asset
def taxi_trips_file() -> None:
    """
    The raw parquet files for the taxi trips dataset. Sourced from the NYC Open Data portal.
    """
    month_to_fetch = "2023-03"
    raw_trips = requests.get(
        f"https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{month_to_fetch}.parquet"
    )

    with open(
        constants.TAXI_TRIPS_TEMPLATE_FILE_PATH.format(month_to_fetch), "wb"
    ) as output_file:
        output_file.write(raw_trips.content)


@dg.asset
def taxi_zones_file() -> None:
    """
    The raw CSV file for the taxi zones dataset. Sourced from the NYC Open Data portal.
    """
    raw_taxi_zones = requests.get(
        "https://community-engineering-artifacts.s3.us-west-2.amazonaws.com/dagster-university/data/taxi_zones.csv"
    )

    with open(constants.TAXI_ZONES_FILE_PATH, "wb") as output_file:
        output_file.write(raw_taxi_zones.content)


@dg.asset(deps=["taxi_trips_file"])
def taxi_trips() -> None:
    """
    The raw taxi trips dataset, loaded into a DuckDB database
    """
    query = """
        create or replace table trips as (
          select
            VendorID as vendor_id,
            PULocationID as pickup_zone_id,
            DOLocationID as dropoff_zone_id,
            RatecodeID as rate_code_id,
            payment_type as payment_type,
            tpep_dropoff_datetime as dropoff_datetime,
            tpep_pickup_datetime as pickup_datetime,
            trip_distance as trip_distance,
            passenger_count as passenger_count,
            total_amount as total_amount
          from 'data/raw/taxi_trips_2023-03.parquet'
        );
    """

    conn = backoff(
        fn=duckdb.connect,
        retry_on=(RuntimeError, duckdb.IOException),
        kwargs={
            "database": os.getenv("DUCKDB_DATABASE"),
        },
        max_retries=10,
    )
    conn.execute(query)


@dg.asset(deps=["taxi_zones_file"])
def taxi_zones() -> None:
    query = f"""
        create or replace table zones as (
            select
                LocationID as zone_id,
                zone,
                borough,
                the_geom as geometry
            from '{constants.TAXI_ZONES_FILE_PATH}'
        );
    """

    conn = backoff(
        fn=duckdb.connect,
        retry_on=(RuntimeError, duckdb.IOException),
        kwargs={
            "database": os.getenv("DUCKDB_DATABASE"),
        },
        max_retries=10,
    )
    conn.execute(query)
