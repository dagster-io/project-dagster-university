with
    raw_trips as (
        select *
        from {{ source('raw_taxis', 'trips') }}
    )
select
    {{
        dbt_utils.generate_surrogate_key([
            'partition_date',
            'pickup_zone_id',
            'dropoff_zone_id',
            'pickup_datetime',
            'dropoff_datetime',
        ])
    }} as trip_id,
    *
from raw_trips