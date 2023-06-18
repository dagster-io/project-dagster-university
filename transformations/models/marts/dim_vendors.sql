with
    int_vendors as (
        select *
        from {{ ref('int_vendors') }}
    )
select
    vendor_id,
    vendor_name
from int_vendors