from dagster import asset
from dagster_duckdb import DuckDBResource

import pandas as pd

from ..partitions import monthly_partition

@asset(
    partitions_def=monthly_partition,
)
def trips_by_month(context, raw_taxi_trips, database: DuckDBResource):
    """
        The number of trips per month, aggregated by month.
    """
    
    partition_date_str = context.asset_partition_key_for_output()
    month_to_fetch = partition_date_str[:-3]

    query = f"""
        select *
        from raw_trips
        where pickup_datetime >= '{month_to_fetch}-01' and pickup_datetime < '{month_to_fetch}-01'::date + interval '1 month'
    """

    with database.get_connection() as conn:
        data_for_month = conn.execute(query).fetch_df()
    
    aggregate = data_for_month.agg({"vendor_id": "count", "total_amount": "sum", "trip_distance": "sum", "passenger_count": "sum"}).rename({"vendor_id": "num_trips"}).to_frame().T # type: ignore

    aggregate["period"] = month_to_fetch
    aggregate['num_trips'] = aggregate['num_trips'].astype(int)
    aggregate['passenger_count'] = aggregate['passenger_count'].astype(int)
    aggregate['total_amount'] = aggregate['total_amount'].round(2).astype(float)
    aggregate['trip_distance'] = aggregate['trip_distance'].round(2).astype(float)
    aggregate = aggregate[["period", "num_trips", "total_amount", "trip_distance", "passenger_count"]]

    try:
        # If the file already exists, append to it, but replace the existing month's data
        existing = pd.read_csv("data/trips_by_month.csv")
        existing = existing[existing["period"] != month_to_fetch]
        existing = pd.concat([existing, aggregate])
        existing.to_csv("data/trips_by_month.csv", index=False)
    except FileNotFoundError:
        aggregate.to_csv("data/trips_by_month.csv", index=False)

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
def trips_by_airport(raw_taxi_trips, raw_taxi_zones, database: DuckDBResource):
    """
        Metrics on taxi trips from the three major NYC airports
    """
    airport_zones = {
        "JFK Airport": "132",
        "LaGuardia Airport": "138",
        "Newark Airport": "1",
    }

    query = f"""
        select
            zone as airport,
            count(1) as num_trips,
            round(sum(total_amount), 2) as total_amount,
            round(sum(trip_distance) / count(1), 2) as avg_trip_distance,
            round(sum(passenger_count) / count(1), 2) as avg_passenger_count,
            round(sum(total_amount) / count(1), 2) as avg_cost_per_trip,
            round(sum(total_amount) / sum(passenger_count), 2) as avg_price_per_passenger
        from raw_trips
        left join raw_taxi_zones on raw_trips.pickup_location_id = raw_taxi_zones.location_id
        where pickup_location_id in ({', '.join(airport_zones.values())})
        group by zone
    """

    with database.get_connection() as conn:
        trips_by_airport = conn.execute(query).fetch_df()
    

    # NOTE: I'm thinking about dropping these calculations, since they're not really necessary for the demo and we're already showing how to do in-memory calculations in trips_by_month
    # zone_combinations_df = pd.read_csv("data/zone_combinations.csv")
    # zone_combinations_df = zone_combinations_df[zone_combinations_df["pickup_zone"].isin(airport_zones.keys())]

    # max_trips = zone_combinations_df.groupby("pickup_zone").agg({"num_trips": "max", "dropoff_zone": "first"}).reset_index()

    # filtered = zone_combinations_df[zone_combinations_df['dropoff_zone'].notnull() & (zone_combinations_df['pickup_zone'] != zone_combinations_df['dropoff_zone'])]

    # most_frequent_combinations = filtered.groupby('pickup_zone').apply(lambda x: x.loc[x['num_trips'].idxmax()]).reset_index(drop=True)

    # trips_by_airport["most_frequent_dropoff_zone"] = trips_by_airport.merge(
    #     most_frequent_combinations,
    #     left_on="zone",
    #     right_on="pickup_zone",
    # )["dropoff_zone"]

    # trips_by_airport["num_trips"] = trips_by_airport.merge(
    #     max_trips,
    #     left_on="zone",
    #     right_on="pickup_zone",
    # )["num_trips_x"]

    # total_trips = trips_by_airport["num_trips"].sum()
    # trips_by_airport["percent_of_total"] = (trips_by_airport["num_trips"] / total_trips).round(4) * 100
    
    trips_by_airport.to_csv("data/trips_by_airport.csv", index=False)