	select
		VendorID as vendor_id,
		PULocationID as pickup_zone_id,
		DOLocationID as dropoff_zone_id,
		RatecodeID as rate_code_id,
		payment_type as payment_type,
		tpep_dropoff_datetime as dropoff_datetime,
		tpep_pickup_datetime as pickup_datetime,
		trip_distance as trip_distance,
		passenger_count as passenger_count,
		total_amount as total_amount
	from 'data/raw/taxi_trips_2023-03.parquet'

