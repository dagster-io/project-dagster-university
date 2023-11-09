with
    staged_trips as (
        select distinct
            rate_code_id
        from {{ ref('stg_trips') }}
    ),
    mapped as (
        select
            {{ dbt_utils.generate_surrogate_key(['rate_code_id'])}} as rate_code_id,
            case rate_code_id
                when 1 then 'Standard rate'
                when 2 then 'JFK'
                when 3 then 'Newark'
                when 4 then 'Nassau or Westchester'
                when 5 then 'Negotiated fare'
                when 6 then 'Group ride'
                when 99 then 'Unknown'
                else 'Unknown'
            end as rate_code
        from staged_trips
    )
select *
from mapped