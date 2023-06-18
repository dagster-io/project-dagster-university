from dagster import asset
from dagster_duckdb import DuckDBResource

import requests

from ..partitions import monthly_partition

@asset(
    group_name="raw_files",
)
def taxi_zones_file():
    """
        The raw CSV file for the taxi zones dataset. Sourced from the NYC Open Data portal.
    """
    raw_taxi_zones = requests.get(
        "https://data.cityofnewyork.us/api/views/755u-8jsi/rows.csv?accessType=DOWNLOAD"
    )

    with open("data/raw/taxi_zones.csv", "wb") as output_file:
        output_file.write(raw_taxi_zones.content)

@asset(
    group_name="ingested",
)
def taxi_zones(taxi_zones_file, database: DuckDBResource):
    """
        The raw taxi zones dataset, loaded into a DuckDB database.
    """

    query = f"""
        create or replace table zones as (
            select
                LocationID as zone_id,
                zone,
                borough,
                the_geom as geometry
            from 'data/raw/taxi_zones.csv'
        );
    """

    with database.get_connection() as conn:
        conn.execute(query)

@asset(
    partitions_def=monthly_partition,
    group_name="raw_files",
)
def taxi_trips_file(context):
    """
        The raw parquet files for the taxi trips dataset. Sourced from the NYC Open Data portal.
    """

    partition_date_str = context.asset_partition_key_for_output()
    month_to_fetch = partition_date_str[:-3]

    raw_trips = requests.get(
        f"https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{month_to_fetch}.parquet"
    )

    with open(f"data/raw/trips-{month_to_fetch}.parquet", "wb") as output_file:
        output_file.write(raw_trips.content)

@asset(
    partitions_def=monthly_partition,
    group_name="ingested",
)
def taxi_trips(context, taxi_trips_file, database: DuckDBResource):
    """
        The raw taxi trips dataset, loaded into a DuckDB database, partitioned by month.
    """

    partition_date_str = context.asset_partition_key_for_output()
    month_to_fetch = partition_date_str[:-3]

    insert_query = f"""
        delete from trips where partition_date = '{month_to_fetch}';
    
        insert into trips
        select
            VendorID, PULocationID, DOLocationID, RatecodeID, payment_type, tpep_dropoff_datetime, 
            tpep_pickup_datetime, trip_distance, passenger_count, store_and_fwd_flag, fare_amount, 
            congestion_surcharge, improvement_surcharge, airport_fee, mta_tax, extra, tip_amount, 
            tolls_amount, total_amount, '{month_to_fetch}' as partition_date
        from 'data/raw/trips-{month_to_fetch}.parquet';
    """

    with database.get_connection() as conn:
        conn.execute(insert_query)