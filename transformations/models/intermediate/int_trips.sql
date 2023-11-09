with
    staged_trips as (
        select *
        from {{ ref('stg_trips') }}
    ),
    mapped as (
        select
            *
            exclude (
                payment_type,
                vendor_id
            ),
            {{ dbt_utils.generate_surrogate_key(['payment_type'])}} as payment_type_id,
            {{ dbt_utils.generate_surrogate_key(['vendor_id'])}} as vendor_id,
        from staged_trips
    )
select *
from mapped