with
    trips as (
        select *
        from {{ ref('stg_trips') }}
    ),
    zones as (
        select *
        from {{ ref('stg_zones') }}
    ),
    trips_by_zone as (
        select
            pickup_zones.zone_name as zone,
            count(*) as trips,
            sum(trips.trip_distance) as total_distance,
            sum(trips.duration) as total_duration,
            sum(trips.total_amount) as fare,
            mode() within group (order by dropoff_zones.zone_name) as most_common_dropoff_zone,
            mode() within group (order by date_part('hour', pickup_datetime)) as most_popular_hour
        from trips
        left join zones as pickup_zones on trips.dropoff_zone_id = pickup_zones.zone_id
        left join zones as dropoff_zones on trips.dropoff_zone_id = dropoff_zones.zone_id
        group by all
    )
select *
from trips_by_zone