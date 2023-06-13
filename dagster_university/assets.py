from dagster import asset, get_dagster_logger
from dagster_duckdb import DuckDBResource

import requests

@asset
def taxi_zones_file():
    raw_taxi_zones = requests.get(
        "https://data.cityofnewyork.us/api/geospatial/d3c5-ddgc?method=export&format=GeoJSON"
    )

    with open("taxi_zones.geojson", "wb") as f:
        f.write(raw_taxi_zones.content)

@asset
def taxi_zones(taxi_zones_file, database: DuckDBResource):
    query = f"""
        create or replace table zones as (
        select
            zone,
            location_id,
            borough,
            st_geomfromwkb(wkb_geometry) as geom 
        from st_read('taxi_zones.geojson')
        );
    """

    with database.get_connection() as conn:
        conn.install_extension("spatial")
        conn.load_extension("spatial")
        conn.execute(query)

@asset
def taxi_trips_file():
    raw_trips = requests.get(
        "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-01.parquet"
    )

    with open("yellow_tripdata_2023-01.parquet", "wb") as f:
        f.write(raw_trips.content)

@asset
def taxi_trips(taxi_trips_file, database: DuckDBResource):
    query = f"""
        create or replace table raw_trips as (
            select *
            from 'yellow_tripdata_2023-01.parquet'
        );
    """

    with database.get_connection() as conn:
        conn.execute(query)