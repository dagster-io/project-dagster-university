with
    staged_trips as (
        select *
        from {{ ref('stg_trips') }}
    ),
    mapped as (
        select
            *
            exclude (
                rate_code_id,
                payment_type,
                vendor_id,
                store_and_forwarded_flag
            ),
            {{ dbt_utils.generate_surrogate_key(['rate_code_id'])}} as rate_code_id,
            {{ dbt_utils.generate_surrogate_key(['payment_type'])}} as payment_type_id,
            {{ dbt_utils.generate_surrogate_key(['vendor_id'])}} as vendor_id,
            case store_and_forwarded_flag
                when 'Y' then true
                when 'N' then false
                else null
            end as was_store_and_forwarded
        from staged_trips
    )
select *
from mapped