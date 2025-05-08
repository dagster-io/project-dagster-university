---
title: "Lesson 3: Partitions"
module: 'dagster_etl'
lesson: '3'
---

# Partitions

When running ETL pipelines in production, it's important to have a reliable way to track what data has been loaded, especially in workflows that handle frequent imports or have a long operational history. Without a structured approach, it can quickly become difficult to manage which data has been processed and which hasn't.

Dagster addresses this challenge with partitions. Partitions allow you to break down your data into smaller, logical segments, such as by date, region, or category — and treat each segment as an independently tracked unit. This makes your pipelines more efficient, scalable, and resilient.

When assets are configured with partitions, you can:

- Materialize and update only specific partitions, avoiding unnecessary reprocessing of unchanged data.
- Launch targeted backfills to reprocess historical data or recover from failures without rerunning the entire pipeline.
- Track the status and lineage of each partition independently, giving you better visibility and control over your data workflows.

## Partitioned assets

Let's go back to our `import_file` asset. What is a logical way to divide that data? Let's say there are 3 files:

- 2018-01-22.csv
- 2018-01-23.csv
- 2018-01-24.csv

Where each file contains data associated with the timestamp on the file. This lends itself to a daily partition. We can configure a daily partition like so:

```python
partitions_def = dg.DailyPartitionsDefinition(
    start_date="2018-01-21",
    end_date="2018-01-24",
)
```

Now that we’ve defined our partition, we can use it in a new asset called `import_partition_file`. This asset will rely on the partition key instead of using a `FilePath` run configuration.

The core logic of the asset remains the same, reading and loading a file, but instead of passing in an arbitrary file path at runtime, the asset will now be executed based on a specific partition value. For example, you can run it for each day between 2018-01-21 and 2018-01-23, with each partition corresponding to a file for that date. This allows you to scale execution, track progress per partition, and reprocess specific days as needed:

```python
@dg.asset(
    partitions_def=partitions_def,
    group_name="static_etl",
)
def import_partition_file(context: dg.AssetExecutionContext) -> str:
    file_path = (
        Path(__file__).absolute().parent
        / f"../../../../data/source/{context.partition_key}.csv"
    )
    return str(file_path.resolve())
```

**Note**: This daily partition has an explicit end date. If we left that off, there would be valid partitions for every day up to the present.

Finally we can add a new downstream asset that loaded the partitioned data into DuckDB:

```python
@dg.asset(
    kinds={"duckdb"},
    partitions_def=partitions_def,
    group_name="static_etl",
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
```
