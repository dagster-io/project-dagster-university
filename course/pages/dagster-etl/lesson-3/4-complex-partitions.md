---
title: "Lesson 3: Complex partitions"
module: 'dagster_etl'
lesson: '3'
---

# Complex partitions

So far, we’ve looked at partitioning data from sources that follow consistent patterns — such as files organized by time intervals (daily, weekly, or monthly). These types of partitions are straightforward to implement and easy to track because the boundaries are predictable.

But what about cases where the upstream data doesn’t follow a fixed pattern? For example, what if the data is grouped by something like customer name? In this case, the set of partitions may evolve over time as new customers are added. We still want each customer to be tracked independently, but we can’t rely on a predefined list.

## Dynamic partitions

Dagster supports dynamic partitions, which give you more flexibility by allowing the set of partitions to be defined and updated at runtime. Unlike static time-based partitions, dynamic partitions let you control exactly what values are included — and grow the partition set as new data categories (like customer names) appear.

Creating a dynamic partition is simple — all you need is a name:

```python
s3_partitions_def = dg.DynamicPartitionsDefinition(name="s3")
```

This defines a dynamic partition set named "s3", which you can later populate and manage based on your data.

## Dynamic partition assets

We can then create a new asset that is the same as our other partitioned asset except it uses the dynamic partition:

```python
@dg.asset(
    partitions_def=s3_partitions_def,
    group_name="static_etl",
)
def import_dynamic_partition_file(context: dg.AssetExecutionContext) -> str:
    file_path = (
        Path(__file__).absolute().parent
        / f"../../../../data/source/{context.partition_key}.csv"
    )
    return str(file_path.resolve())
```

If you attempted to execute this asset in Dagster, you’d notice that it cannot be materialized right away — that's because no partitions have been defined yet. This behavior makes sense: dynamic partitions are empty by default and have no built-in logic to determine which partition keys should exist. It’s up to you to register the partition values you want Dagster to track.

To move forward, let’s define a downstream asset that loads data into DuckDB, using the values from our dynamic partition (e.g., customer names). This asset will read and process data based on the partition key, ensuring each customer’s data is handled independently and reproducibly:

```python
@dg.asset(
    kinds={"duckdb"},
    partitions_def=s3_partitions_def,
    group_name="static_etl",
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
```

This setup should look very similar to the daily partition we created earlier. But how does it play out in practice? To better understand the distinction, let’s dive into the differences in how partitioned pipelines are triggered — specifically comparing time-based (e.g., daily) partitions with dynamic ones. Each type requires a different approach to scheduling and orchestration, depending on how and when new data becomes available.
