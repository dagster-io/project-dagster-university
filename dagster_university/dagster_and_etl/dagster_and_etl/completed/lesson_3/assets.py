import csv
from pathlib import Path

import dagster as dg
from dagster_duckdb import DuckDBResource

# Example 1 - Load with asset check
# Showcase
# - Configs
# - Asset checks


class FilePath(dg.Config):
    path: str


@dg.asset
def import_file(context: dg.AssetExecutionContext, config: FilePath) -> str:
    file_path = Path(__file__).absolute().parent / f"../../../data/source/{config.path}"
    return str(file_path.resolve())


@dg.asset_check(
    asset=import_file,
    blocking=True,
    description="Ensure file is not empty",
)
def not_empty(
    context: dg.AssetCheckExecutionContext,
    import_file,
) -> dg.AssetCheckResult:
    with open(import_file, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]

    if len(data) > 0:
        return dg.AssetCheckResult(
            passed=True,
            metadata={"number of rows": len(data)},
        )

    return dg.AssetCheckResult(
        passed=True,
        metadata={"number of rows": len(data)},
    )


@dg.asset
def duckdb_table(
    context: dg.AssetExecutionContext,
    database: DuckDBResource,
    import_file,
):
    table_name = "raw_data"
    with database.get_connection() as conn:
        table_query = f"""
            create table if not exists {table_name} (
                date date,
                share_price float,
                amount float,
                spend float,
                shift float,
                spread float
            ) 
        """
        conn.execute(table_query)
        conn.execute(f"COPY {table_name} FROM '{import_file}';")


# Example 2 - Scheduled Partition
# Showcase
# - Partition
# - Schedule
partitions_def = dg.DailyPartitionsDefinition(
    start_date="2018-01-21",
    end_date="2018-01-24",
)


@dg.asset(
    partitions_def=partitions_def,
)
def import_partition_file(context: dg.AssetExecutionContext) -> str:
    file_path = (
        Path(__file__).absolute().parent
        / f"../../../data/source/{context.partition_key}.csv"
    )
    return str(file_path.resolve())


@dg.asset(
    partitions_def=partitions_def,
)
def duckdb_partition_table(
    context: dg.AssetExecutionContext,
    database: DuckDBResource,
    import_partition_file,
):
    table_name = "raw_partition_data"
    with database.get_connection() as conn:
        table_query = f"""
            create table if not exists {table_name} (
                date date,
                share_price float,
                amount float,
                spend float,
                shift float,
                spread float
            ) 
        """
        conn.execute(table_query)
        conn.execute(f"COPY {table_name} FROM '{import_partition_file}';")


# Example 3 - Event Driven Partition
# Showcase
# - Dynamic Partition
# - Sensors


s3_partitions_def = dg.DynamicPartitionsDefinition(name="s3")


@dg.asset(
    partitions_def=s3_partitions_def,
)
def import_dynamic_partition_file(context: dg.AssetExecutionContext) -> str:
    file_path = (
        Path(__file__).absolute().parent
        / f"../../../data/source/{context.partition_key}.csv"
    )
    return str(file_path.resolve())


@dg.asset(
    partitions_def=s3_partitions_def,
)
def duckdb_dynamic_partition_table(
    context: dg.AssetExecutionContext,
    database: DuckDBResource,
    import_dynamic_partition_file,
):
    table_name = "raw_partition_data"
    with database.get_connection() as conn:
        table_query = f"""
            create table if not exists {table_name} (
                date date,
                share_price float,
                amount float,
                spend float,
                shift float,
                spread float
            ) 
        """
        conn.execute(table_query)
        conn.execute(f"COPY {table_name} FROM '{import_dynamic_partition_file}'")
