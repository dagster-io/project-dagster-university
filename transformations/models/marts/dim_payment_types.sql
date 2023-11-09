with
    int_payment_types as (
        select *
        from {{ ref('int_payment_types') }}
    )
select
    payment_type_id,
    payment_type
from int_payment_types