from dagster import asset, get_dagster_logger
from dagster_duckdb import DuckDBResource

import requests
import tempfile

@asset
def taxi_zones(database: DuckDBResource):
    raw_taxi_zones = requests.get(
        "https://data.cityofnewyork.us/api/geospatial/d3c5-ddgc?method=export&format=GeoJSON"
    ).content

    with tempfile.NamedTemporaryFile(suffix=".geojson") as tmpfile:
        with open(tmpfile.name, "wb") as f:
            f.write(raw_taxi_zones)

        query = f"""
            create or replace table zones as (
            select
                zone,
                location_id,
                borough,
                st_geomfromwkb(wkb_geometry) as geom 
            from st_read('{tmpfile.name}')
            );
        """

        with database.get_connection() as conn:
            conn.install_extension("spatial")
            conn.load_extension("spatial")
            conn.execute(query)

@asset
def taxi_trips(database: DuckDBResource):
    raw_trips = requests.get(
        "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-01.parquet"
    ).content

    with tempfile.NamedTemporaryFile(suffix=".parquet") as tmpfile:
        with open(tmpfile.name, "wb") as f:
            f.write(raw_trips)
        
        query = f"""
            create or replace table raw_trips as (
                select *
                from '{tmpfile.name}'
            );
        """

        with database.get_connection() as conn:
            conn.execute(query)