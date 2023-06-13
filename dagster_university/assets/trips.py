from dagster import asset
from dagster_duckdb import DuckDBResource

import requests

from ..partitions import monthly_partitions

@asset
def taxi_zones_file():
    raw_taxi_zones = requests.get(
        "https://data.cityofnewyork.us/api/views/755u-8jsi/rows.csv?accessType=DOWNLOAD"
    )

    with open("taxi_zones.csv", "wb") as f:
        f.write(raw_taxi_zones.content)

@asset
def taxi_zones(taxi_zones_file, database: DuckDBResource):
    query = f"""
        create or replace table zones as (
            select
                LocationID as location_id,
                zone,
                borough
            from 'taxi_zones.csv'
        );
    """

    with database.get_connection() as conn:
        conn.execute(query)

@asset(
    partitions_def=monthly_partitions,
)
def taxi_trips_file(context):
    partition_date_str = context.asset_partition_key_for_output()
    month_to_fetch = partition_date_str[:-3]

    raw_trips = requests.get(
        f"https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{month_to_fetch}.parquet"
    )

    with open(f"trips-{month_to_fetch}.parquet", "wb") as f:
        f.write(raw_trips.content)

@asset(
    partitions_def=monthly_partitions,
)
def taxi_trips(context, taxi_trips_file, database: DuckDBResource):
    partition_date_str = context.asset_partition_key_for_output()
    month_to_fetch = partition_date_str[:-3]

    create_query = """
        create table if not exists raw_trips (
            vendor_id integer,
            pickup_location_id integer,
            dropoff_location_id integer,
            rate_code_id double,
            payment_type integer,
            dropoff_datetime timestamp,
            pickup_datetime timestamp,
            trip_distance double,
            passenger_count double,
            store_and_forwarded_flag varchar,
            fare_amount double,
            congestion_surcharge double,
            improvement_surcharge double,
            airport_fee double,
            mta_tax double,
            extra double,
            tip_amount double,
            tolls_amount double,
            total_amount double,
            partition_date varchar
        );
    """

    insert_query = f"""
        delete from raw_trips where partition_date = '{month_to_fetch}';
    
        insert into raw_trips
        select
            VendorID, PULocationID, DOLocationID, RatecodeID, payment_type, tpep_dropoff_datetime, 
            tpep_pickup_datetime, trip_distance, passenger_count, store_and_fwd_flag, fare_amount, 
            congestion_surcharge, improvement_surcharge, airport_fee, mta_tax, extra, tip_amount, 
            tolls_amount, total_amount, '{month_to_fetch}' as partition_date
        from 'trips-{month_to_fetch}.parquet';
    """

    with database.get_connection() as conn:
        conn.execute(create_query)
        conn.execute(insert_query)