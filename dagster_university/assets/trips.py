from dagster import asset, MetadataValue
from dagster_duckdb import DuckDBResource

import requests

from . import constants

from ..partitions import monthly_partition

## Lesson 3 (change this to HW)
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

    with open(constants.TAXI_ZONES_FILE_PATH, "wb") as output_file:
        output_file.write(raw_taxi_zones.content)

## Lesson 4 (HW) , 6
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
            from '{constants.TAXI_ZONES_FILE_PATH}'
        );
    """

    with database.get_connection() as conn:
        conn.execute(query)

## Lesson 3, 8
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

    with open(constants.TAXI_TRIPS_TEMPLATE_FILE_PATH.format(month_to_fetch), "wb") as output_file:
        output_file.write(raw_trips.content)
    context.add_output_metadata({'Number of records': MetadataValue.int(len(raw_trips.content))})
    

## Lesson 4, 8, 6
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

    query = f"""
        create table if not exists trips (
            vendor_id integer, pickup_zone_id integer, dropoff_zone_id integer,
            rate_code_id double, payment_type integer, dropoff_datetime timestamp,
            pickup_datetime timestamp, trip_distance double, passenger_count double,
            store_and_forwarded_flag varchar, fare_amount double, congestion_surcharge double,
            improvement_surcharge double, airport_fee double, mta_tax double,
            extra double, tip_amount double, tolls_amount double,
            total_amount double, partition_date varchar
        );

        delete from trips where partition_date = '{month_to_fetch}';
    
        insert into trips
        select
            VendorID, PULocationID, DOLocationID, RatecodeID, payment_type, tpep_dropoff_datetime, 
            tpep_pickup_datetime, trip_distance, passenger_count, store_and_fwd_flag, fare_amount, 
            congestion_surcharge, improvement_surcharge, airport_fee, mta_tax, extra, tip_amount, 
            tolls_amount, total_amount, '{month_to_fetch}' as partition_date
        from '{constants.TAXI_TRIPS_TEMPLATE_FILE_PATH.format(month_to_fetch)}';
    """

    with database.get_connection() as conn:
        conn.execute(query)