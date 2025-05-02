---
title: "Lesson 3: Partitions"
module: 'dagster_etl'
lesson: '3'
---

## Partitions

When we run ETL pipelines in production we want a better way to track what we have loaded. This can be difficult in pipelines that have a long history of events or import data frequently.

In Dagster this can be handled with partitions. Partitions enable you to manage, process, and track large datasets more efficiently by dividing data into smaller, logical segments. Each partition represents a subset of your data (for example, a specific day, region, or category).

When assets are configured with partitions we can:

- Materialize and update only the relevant subset of data, rather than reprocessing everything.
- Launch backfills for specific partitions, making it easier to recover from failures or reprocess historical data.
- Track the status and lineage of each partition independently, providing better observability and operational control.

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

Now that we have our partition we can supply it to our `import_file` asset. We we create a new asset called `import_partition_file` that relies on the partition we just created rather than the `FilePath` run configuration.

The rest of the asset code will remain the same, but now instead of taking in any arbitrary file path set at execution, the asset can be executed with any number of partitions for each day between 2018-01-21 and 2018-01-23.

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

**Note**: This daily partition has an explicit end date. If we left that off, there would be valid parititons for every day up to the present.

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
