import dagster as dg

postgres_refresh_job = dg.define_asset_job(
    "postgres_refresh",
    selection=[
        dg.AssetKey(["target", "data", "customers"]),
        dg.AssetKey(["target", "data", "products"]),
        dg.AssetKey(["target", "data", "orders"]),
    ],
)

orders_refresh_job = dg.define_asset_job(
    "orders_refresh",
    selection=[
        dg.AssetKey(["target", "data", "orders"]),
    ],
)
