with
    int_rate_codes as (
        select *
        from {{ ref('int_rate_codes') }}
    )
select
    rate_code_id,
    rate_code
from int_rate_codes