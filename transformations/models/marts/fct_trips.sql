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
    payment_type_id,
    dropoff_datetime,
    pickup_datetime,
    passenger_count,
    total_amount,
    trip_distance
from intermediate_trips