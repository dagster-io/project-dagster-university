from dagster import asset
from dagster_duckdb import DuckDBResource

import pandas as pd
import requests

from ..partitions import monthly_partitions

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

    with open("data/taxi_zones.csv", "wb") as output_file:
        output_file.write(raw_taxi_zones.content)

@asset(
    group_name="ingested",
)
def raw_taxi_zones(taxi_zones_file, database: DuckDBResource):
    """
        The raw taxi zones dataset, loaded into a DuckDB database.
    """

    query = f"""
        create or replace table raw_taxi_zones as (
            select
                LocationID as location_id,
                zone,
                borough,
                the_geom as zone_polygon
            from 'data/taxi_zones.csv'
        );
    """

    with database.get_connection() as conn:
        conn.execute(query)

@asset(
    partitions_def=monthly_partitions,
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

    with open(f"data/trips-{month_to_fetch}.parquet", "wb") as output_file:
        output_file.write(raw_trips.content)

@asset(
    partitions_def=monthly_partitions,
    group_name="ingested",
)
def raw_taxi_trips(context, taxi_trips_file, database: DuckDBResource):
    """
        The raw taxi trips dataset, loaded into a DuckDB database, partitioned by month.
    """

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
        from 'data/trips-{month_to_fetch}.parquet';
    """

    with database.get_connection() as conn:
        conn.execute(create_query)
        conn.execute(insert_query)

@asset(
    group_name="metrics"
)
def trips_by_month(raw_taxi_trips, database: DuckDBResource):
    """
        The number of trips per month, aggregated by month.
    """

    query = """
        select
            date_trunc('month', dropoff_datetime) as month,
            count(*) as num_trips,
            sum(total_amount) as revenue,            
        from raw_trips
        group by 1
        order by 3, 2 desc;
    """

    with database.get_connection() as conn:
        df = conn.execute(query).fetch_df()

    df.to_csv("data/trips_by_month.csv", index=False)

@asset(
    group_name="metrics"
)
def zone_combinations(raw_taxi_trips, raw_taxi_zones, database: DuckDBResource):
    """
        The number of trips between each pair of taxi zones.
    """

    query = """
        with combinations as (
            select
                pickup_location_id,
                dropoff_location_id,
                count(1) as num_trips
            from raw_trips
            group by pickup_location_id, dropoff_location_id
        )
        select
            pickup_zone.zone as pickup_zone,
            dropoff_zone.zone as dropoff_zone,
            num_trips
        from combinations
        left join raw_taxi_zones as pickup_zone on combinations.pickup_location_id = pickup_zone.location_id
        left join raw_taxi_zones as dropoff_zone on combinations.dropoff_location_id = dropoff_zone.location_id
    """

    with database.get_connection() as conn:
        df = conn.execute(query).fetch_df()

    df.to_csv("data/zone_combinations.csv", index=False)    

@asset(
    group_name="metrics"
)
def trips_by_airport(raw_taxi_trips, raw_taxi_zones, zone_combinations, database: DuckDBResource):
    """
        Metrics on taxi trips from the three major NYC airports.
        Percentage of total airport trips is calculated by dividing the number of trips from a given airport by the total number of trips from all airports.
    """
    airport_zones = {
        "JFK Airport": "132",
        "LaGuardia Airport": "138",
        "Newark Airport": "1",
    }

    query = f"""
        select
            zone,
            count(1) as num_trips
        from raw_trips
        left join raw_taxi_zones on raw_trips.pickup_location_id = raw_taxi_zones.location_id
        where pickup_location_id in ({', '.join(airport_zones.values())})
        group by zone
    """

    with database.get_connection() as conn:
        trips_by_airport = conn.execute(query).fetch_df()
    
    zone_combinations_df = pd.read_csv("data/zone_combinations.csv")
    zone_combinations_df = zone_combinations_df[zone_combinations_df["pickup_zone"].isin(airport_zones.keys())]

    max_trips = zone_combinations_df.groupby("pickup_zone").agg({"num_trips": "max"}).reset_index()

    trips_by_airport = trips_by_airport.merge(max_trips, left_on="zone", right_on="pickup_zone")
    total_airport_trips = trips_by_airport["num_trips_x"].sum()

    trips_by_airport["percent_of_total"] = (trips_by_airport["num_trips_x"] / total_airport_trips).round(4) * 100
    trips_by_airport = trips_by_airport.drop(columns=["num_trips_y"]).rename(columns={"num_trips_x": "num_trips"})
    
    trips_by_airport.to_csv("data/trips_by_airport.csv", index=False)