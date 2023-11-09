with
    staged_trips as (
        select distinct
            vendor_id
        from {{ ref('stg_trips') }}
    ),
    mapped as (
        select
            {{ dbt_utils.generate_surrogate_key(['vendor_id'])}} as vendor_id,
            case vendor_id
                when '1' then 'Creative Mobile Technologies, LLC'
                when '2' then 'VeriFone Inc.'
                else 'Unknown'
            end as vendor_name
        from staged_trips
    )
select *
from mapped