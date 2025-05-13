---
title: "Lesson 3: Partitions"
module: 'dagster_etl'
lesson: '3'
---

# Partitions

When running ETL pipelines in production, it's important to have a reliable way to track what data has been loaded, especially when a pipeline has matured and has a longer execution history.

Without a structured approach, it can become difficult to manage which data has been processed and which hasn't. Dagster addresses this challenge with partitions. Partitions allow you to break down your data into smaller, logical segments: such as by date, region, or category. Each segment can then be treated and tacked as an independent unit.

When assets are configured with partitions, you can:

- Materialize and update only specific partitions, avoiding unnecessary reprocessing of unchanged data.
- Launch targeted backfills to reprocess historical data or recover from failures without rerunning the entire pipeline.
- Track the status and lineage of each partition independently, giving you better visibility and control over your data workflows.

## Partitioned assets

Let's go back to our `import_file` asset. What is a logical way to divide that data if our three files look like this?

- 2018-01-22.csv
- 2018-01-23.csv
- 2018-01-24.csv

Based on these files it would be safe to assume that each one corresponds to a specific day. This lends itself to a daily partition which we can configure with Dagster like so:

```python
partitions_def = dg.DailyPartitionsDefinition(
    start_date="2018-01-21",
    end_date="2018-01-24",
)
```

Now that we’ve defined our partition, we can use the partition in a new asset called `import_partition_file`. This asset will rely on the partition key instead of the `FilePath` run configuration to determine which file should be processed.

The core logic of the asset remains the same but now you can run the pipeline for each day between 2018-01-21 and 2018-01-23, with each partition corresponding to a file for that date. This allows you to scale execution, track progress per partition, and reprocess specific days as needed:

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

**Note**: This daily partition we are using in this example has an explicit end date. If we left that off, there would be valid partitions for every day from the start of the partition to the current day.

Finally we can create a new downstream asset that relies on the partitioned data:

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

Again none of the logic is different though we are including the partition in the `dg.asset` decorator.
