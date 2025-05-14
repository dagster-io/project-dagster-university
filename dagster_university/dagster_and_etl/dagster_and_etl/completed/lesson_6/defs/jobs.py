import dagster as dg

postgres_refresh_job = dg.define_asset_job(
    "postgres_refresh", selection=["customers", "products", "orders"]
)

orders_refresh_job = dg.define_asset_job("orders_refresh", selection=["orders"])
