with raw_zones as (
    select *
    from {{ source('raw_taxis', 'zones') }}
)
select
    zone_id,
    zone as zone_name,
    borough,
    zone_name like '%Airport' as is_airport,
    -- zone_population -- new column
from raw_zones