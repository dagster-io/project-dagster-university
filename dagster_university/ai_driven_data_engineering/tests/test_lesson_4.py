import dagster as dg

from ai_driven_data_engineering.completed.lesson_4.defs.assets import raw_data
from ai_driven_data_engineering.completed.lesson_4.defs.schedules import daily_raw


def test_raw_assets_materialize(duckdb_resource):
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
    result = dg.materialize(
        assets=[raw_data.raw_customers],
        resources={"duckdb": duckdb_resource},
    )
    assert result.success
    materializations = result.asset_materializations_for_node("raw_customers")
    row_count = materializations[0].metadata["row_count"].value
    assert row_count > 0


def test_raw_ingestion_job_exists():
    assert daily_raw.raw_ingestion_job is not None
    assert daily_raw.raw_ingestion_job.name == "raw_ingestion_job"


def test_daily_raw_schedule_exists():
    assert daily_raw.daily_raw_schedule is not None
    assert daily_raw.daily_raw_schedule.name == "daily_raw_8am_est"
    assert daily_raw.daily_raw_schedule.cron_schedule == "0 8 * * *"
    assert daily_raw.daily_raw_schedule.execution_timezone == "America/New_York"
    assert daily_raw.daily_raw_schedule.job == daily_raw.raw_ingestion_job
