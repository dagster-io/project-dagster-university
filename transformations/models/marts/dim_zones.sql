with
    int_zones as (
        select *
        from {{ ref('int_zones') }}
    )
select
    zone_id,
    zone_name,
    borough,
    is_airport
from int_zones