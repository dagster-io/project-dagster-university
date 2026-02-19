import dagster as dg
import pytest

from ai_driven_data_engineering.defs.assets import raw_data


def test_raw_assets_materialize(duckdb_resource):
    """Raw assets can be materialized with a DuckDB resource."""
    result = dg.materialize(
        assets=[
            raw_data.raw_customers,
            raw_data.raw_orders,
            raw_data.raw_payments,
        ],
        resources={"duckdb": duckdb_resource},
    )
    assert result.success

    for node_name in ["raw_customers", "raw_orders", "raw_payments"]:
        materializations = result.asset_materializations_for_node(node_name)
        assert len(materializations) > 0
        assert "row_count" in materializations[0].metadata


def test_raw_customers_row_count(duckdb_resource):
    """raw_customers loads and reports row count in metadata."""
    result = dg.materialize(
        assets=[raw_data.raw_customers],
        resources={"duckdb": duckdb_resource},
    )
    assert result.success
    materializations = result.asset_materializations_for_node("raw_customers")
    assert len(materializations) > 0
    row_count = materializations[0].metadata["row_count"].value
    assert row_count > 0
