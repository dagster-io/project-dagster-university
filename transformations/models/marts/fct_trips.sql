with
    intermediate_trips as (
        select *
        from {{ ref('int_trips') }}
    )
select
    trip_id,

    vendor_id,
    pickup_zone_id,
    dropoff_zone_id,
    rate_code_id,
    payment_type_id,
    
    dropoff_datetime,
    pickup_datetime,

    was_store_and_forwarded,
    partition_date,

    airport_fee,
    congestion_surcharge,
    extra,
    fare_amount,
    improvement_surcharge,
    mta_tax,
    passenger_count,
    tip_amount,
    tolls_amount,
    total_amount,
    trip_distance
from intermediate_trips