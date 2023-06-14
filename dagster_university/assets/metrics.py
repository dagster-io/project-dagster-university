from dagster import asset
from dagster_duckdb import DuckDBResource

import pandas as pd

@asset
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

@asset
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

@asset
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