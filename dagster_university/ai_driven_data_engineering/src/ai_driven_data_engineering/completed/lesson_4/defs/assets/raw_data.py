import dagster as dg
from dagster_duckdb import DuckDBResource

RAW_CUSTOMERS_URL = "https://raw.githubusercontent.com/dbt-labs/jaffle-shop-classic/refs/heads/main/seeds/raw_customers.csv"
RAW_ORDERS_URL = "https://raw.githubusercontent.com/dbt-labs/jaffle-shop-classic/refs/heads/main/seeds/raw_orders.csv"
RAW_PAYMENTS_URL = "https://raw.githubusercontent.com/dbt-labs/jaffle-shop-classic/refs/heads/main/seeds/raw_payments.csv"


def _make_raw_asset(name: str, url: str) -> dg.AssetsDefinition:
    @dg.asset(name=name, group_name="raw")
    def _asset(
        context: dg.AssetExecutionContext, duckdb: DuckDBResource
    ) -> dg.MaterializeResult:
        with duckdb.get_connection() as conn:
            conn.execute(f"""
                CREATE OR REPLACE TABLE {name} AS
                SELECT * FROM read_csv_auto('{url}')
            """)
            row_count = conn.execute(f"SELECT COUNT(*) FROM {name}").fetchone()[0]

        context.log.info(f"Loaded {row_count} rows into {name}")
        return dg.MaterializeResult(
            metadata={"row_count": dg.MetadataValue.int(row_count)}
        )

    return _asset


raw_customers = _make_raw_asset("raw_customers", RAW_CUSTOMERS_URL)
raw_orders = _make_raw_asset("raw_orders", RAW_ORDERS_URL)
raw_payments = _make_raw_asset("raw_payments", RAW_PAYMENTS_URL)
