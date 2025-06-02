import csv
from pathlib import Path

import dagster as dg
from dagster_duckdb import DuckDBResource

# Example 1 - Load with asset check
# Showcase
# - Configs
# - Asset checks


class IngestionFileConfig(dg.Config):
    path: str


@dg.asset()
def import_file(context: dg.AssetExecutionContext, config: IngestionFileConfig) -> str:
    file_path = (
        Path(__file__).absolute().parent / f"../../../../data/source/{config.path}"
    )
    return str(file_path.resolve())


@dg.asset_check(
    asset=import_file,
    blocking=True,
    description="Ensure file contains no zero value shares",
)
def invalid_share_price(
    context: dg.AssetCheckExecutionContext,
    import_file,
) -> dg.AssetCheckResult:
    with open(import_file, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        data = (row for row in reader)

        for row in data:
            if float(row["share_price"]) <= 0:
                return dg.AssetCheckResult(
                    passed=False,
                    metadata={"'share' is below 0": row},
                )

    return dg.AssetCheckResult(
        passed=True,
    )


@dg.asset(
    kinds={"duckdb"},
)
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
        conn.execute(f"copy {table_name} from '{import_file}';")


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
        / f"../../../../data/source/{context.partition_key}.csv"
    )
    return str(file_path.resolve())


@dg.asset(
    kinds={"duckdb"},
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
        conn.execute(
            f"DELETE FROM {table_name} WHERE date = '{context.partition_key}';"
        )
        conn.execute(f"copy {table_name} from '{import_partition_file}';")


# Example 3 - Event Driven Partition
# Showcase
# - Dynamic Partition
# - Sensors


dynamic_partitions_def = dg.DynamicPartitionsDefinition(name="dynamic_partition")


@dg.asset(
    partitions_def=dynamic_partitions_def,
)
def import_dynamic_partition_file(context: dg.AssetExecutionContext) -> str:
    file_path = (
        Path(__file__).absolute().parent
        / f"../../../../data/source/{context.partition_key}.csv"
    )
    return str(file_path.resolve())


@dg.asset(
    kinds={"duckdb"},
)
def duckdb_dynamic_partition_table(
    context: dg.AssetExecutionContext,
    database: DuckDBResource,
    import_dynamic_partition_file,
):
    table_name = "raw_dynamic_partition_data"
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
        conn.execute(
            f"DELETE FROM {table_name} WHERE date = '{context.partition_key}';"
        )
        conn.execute(f"copy {table_name} from '{import_dynamic_partition_file}'")


# Example 4 - Cloud Storage
# Showcase
# - Cloud Storage


class IngestionFileS3Config(dg.Config):
    bucket: str
    path: str


@dg.asset(
    kinds={"s3"},
)
def import_file_s3(
    context: dg.AssetExecutionContext,
    config: IngestionFileS3Config,
) -> str:
    s3_path = f"s3://{config.bucket}/{config.path}"
    return s3_path


@dg.asset(
    kinds={"duckdb"},
)
def duckdb_table_s3(
    context: dg.AssetExecutionContext,
    database: DuckDBResource,
    import_file_s3: str,
):
    table_name = "raw_s3_data"
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
        conn.execute(f"copy {table_name} from '{import_file_s3}' (format csv, header);")
