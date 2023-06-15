from dagster import asset
from dagster_duckdb import DuckDBResource
from dagster import MetadataValue, Output
import seaborn
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import pandas as pd

from ..partitions import monthly_partition

@asset(
    partitions_def=monthly_partition,
)
def trips_by_month(context, raw_taxi_trips, database: DuckDBResource):
    """
        The number of trips per month, aggregated by month.
        These date-based aggregations are done in-memory, which is expensive, but enables you to do time-based aggregations consistently across data warehouses (ex. DuckDB and BigQuery)
    """
    
    partition_date_str = context.asset_partition_key_for_output()
    month_to_fetch = partition_date_str[:-3]

    # get all trips for the month
    query = f"""
        select vendor_id, total_amount, trip_distance, passenger_count
        from raw_trips
        where pickup_datetime >= '{month_to_fetch}-01' and pickup_datetime < '{month_to_fetch}-01'::date + interval '1 month'
    """

    with database.get_connection() as conn:
        data_for_month = conn.execute(query).fetch_df()
    
    aggregate = data_for_month.agg({
        "vendor_id": "count",
        "total_amount": "sum",
        "trip_distance": "sum",
        "passenger_count": "sum"
    }).rename({"vendor_id": "num_trips"}).to_frame().T # type: ignore

    # clean up the formatting of the dataframe
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
def trips_by_airport(raw_taxi_trips, raw_taxi_zones, database: DuckDBResource):
    """
        Metrics on taxi trips from the three major NYC airports
    """

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
        where raw_taxi_zones like '%Airport'
        group by zone
    """

    with database.get_connection() as conn:
        trips_by_airport = conn.execute(query).fetch_df()
     
    trips_by_airport.to_csv("data/trips_by_airport.csv", index=False)


@asset()
def airport_pickup_trips(raw_taxi_trips, database: DuckDBResource):


    query = f"""
        select *
        from raw_trips
    """

    with database.get_connection() as conn:
        raw_trip_dataframe = conn.execute(query).fetch_df()
    airport_trips = raw_trip_dataframe[raw_trip_dataframe.pickup_location_id.isin([1, 138, 132]) 
                                        # | raw_trip_dataframe.dropoff_location_id.isin([1, 138, 132])
                                        ]
    
    airport_zones = {132: "JFK Airport",
                  138: "LaGuardia Airport", 
                  1: "Newark Airport"
                  }
    airport_trips['airport_pickup_name'] = airport_trips.pickup_location_id.map(airport_zones)
    plt.clf()
    my_plot = seaborn.boxplot(x='airport_pickup_name', y='total_amount', data=airport_trips)
    fig = my_plot.get_figure()
    buffer = BytesIO()
    fig.savefig(buffer)
    image_data = base64.b64encode(buffer.getvalue())
    airport_plot = MetadataValue.md(f"![img](data:image/png;base64,{image_data.decode()})")
    
    return Output(airport_trips, metadata= {"airport plot":airport_plot})