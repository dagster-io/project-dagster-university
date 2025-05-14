import dagster as dg


@dg.asset(deps=[dg.AssetKey("orders")])
def downstream_orders(context: dg.AssetExecutionContext):
    pass


@dg.asset(deps=[dg.AssetKey("products")])
def downstream_products(context: dg.AssetExecutionContext):
    pass


@dg.asset(deps=[downstream_orders, downstream_products])
def downstream_orders_and_products(context: dg.AssetExecutionContext):
    pass
