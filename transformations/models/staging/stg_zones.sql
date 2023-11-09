with raw_zones as (
    select *
    from {{ source('raw_taxis', 'zones') }}
)
select
    {{ dbt_utils.generate_surrogate_key(['zone_id']) }} as zone_id,
    zone as zone_name,
    borough
from raw_zones