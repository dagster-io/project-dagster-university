with
    staged_trips as (
        select distinct
            payment_type
        from {{ ref('stg_trips') }}
    ),
    mapped as (
        select
            payment_type as raw_payment_type,
            {{ dbt_utils.generate_surrogate_key(['payment_type'])}} as payment_type_id,
            case payment_type
                when 0 then 'Unknown'
                when 1 then 'Credit Card'
                when 2 then 'Cash'
                when 3 then 'No Charge'
                when 4 then 'Dispute'
                when 5 then 'Unknown'
                when 6 then 'Voided Trip'
            end as payment_type
        from staged_trips
    )
select *
from mapped