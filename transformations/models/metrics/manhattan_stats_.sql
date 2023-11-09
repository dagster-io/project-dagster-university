        select
            zones.zone,
            zones.borough,
            zones.geometry,
            count(1) as num_trips,
        from {{ref('fct_trips')}} as trips 
        left join {{ref('dim_zones')}}  as zones on trips.pickup_zone_id = zones.zone_id
        where geometry is not null
        group by zone, borough, geometry