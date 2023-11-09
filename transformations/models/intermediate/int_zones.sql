with
    staged_zones as (
        select *
        from {{ ref('stg_zones') }}
    )
select
    *,
    zone_name like '%Airport' as is_airport
from staged_zones