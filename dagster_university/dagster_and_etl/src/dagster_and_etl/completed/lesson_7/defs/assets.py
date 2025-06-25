import dagster as dg


@dg.asset(deps=["orders"])
def downstream_orders(context: dg.AssetExecutionContext):
    pass


@dg.asset(deps=["products"])
def downstream_products(context: dg.AssetExecutionContext):
    pass


@dg.asset(deps=[downstream_orders, downstream_products])
def downstream_orders_and_products(context: dg.AssetExecutionContext):
    pass
