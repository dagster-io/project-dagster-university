
# Explanation: the Dagster University project uses a DuckDB database to store the data for the NYC Taxi Pipeline.
# For convenience, some tables were created ahead of time and saved within the data.duckdb file.
# If that database file is lost or corrupted, you can recreate the tables by executing the following SQL statements to create a new data.duckdb file.

query = """
    create table if not exists trips (
        vendor_id integer,
        pickup_zone_id integer,
        dropoff_zone_id integer,
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