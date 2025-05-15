import dagster as dg
from dagster_sling import SlingResource, sling_assets

replication_config = dg.file_relative_path(__file__, "sling_replication.yaml")


@sling_assets(replication_config=replication_config)
def postgres_sling_assets(context, sling: SlingResource):
    yield from sling.replicate(context=context).fetch_column_metadata()


@dg.asset(deps=[dg.AssetKey("orders")])
def downstream_orders(context: dg.AssetExecutionContext):
    pass


@dg.asset(deps=[dg.AssetKey("products")])
def downstream_products(context: dg.AssetExecutionContext):
    pass


@dg.asset(deps=[downstream_orders, downstream_products])
def downstream_orders_and_products(context: dg.AssetExecutionContext):
    pass
