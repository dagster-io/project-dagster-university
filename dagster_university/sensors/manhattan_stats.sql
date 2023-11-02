        select
            zones.zone,
            zones.borough,
            zones.geometry,
            count(1) as num_trips,
        from {{ref('trips')}}
        left join {{ref('zones')}} on trips.pickup_zone_id = zones.zone_id
        where geometry is not null
        group by zone, borough, geometry