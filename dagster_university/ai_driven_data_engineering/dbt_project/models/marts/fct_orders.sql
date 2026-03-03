with orders as (
    select * from {{ ref('stg_orders') }}
),

customers as (
    select * from {{ ref('stg_customers') }}
),

payments as (
    select
        order_id,
        sum(amount) as total_amount,
        string_agg(payment_method, ', ') as payment_methods
    from {{ ref('stg_payments') }}
    group by order_id
),

final as (
    select
        orders.order_id,
        orders.customer_id,
        customers.first_name,
        customers.last_name,
        orders.order_date,
        orders.status,
        payments.total_amount,
        payments.payment_methods
    from orders
    left join customers on orders.customer_id = customers.customer_id
    left join payments on orders.order_id = payments.order_id
)

select * from final
