---
title: "Lesson 3: Complex partitions"
module: 'dagster_etl'
lesson: '3'
---

# Complex partitions

Time based partitions are usually easy to implement. They follow consistent patterns, such as daily, weekly, or monthly, and have predictable boundaries.

But what about cases where the upstream data doesn’t follow a fixed pattern? For example, what if the data is grouped by something like customer name? In this case, the set of partitions may evolve over time as new customers are added.

How could we handle this with partitions to ensure we can still track our inputs if they follow an irregular pattern.

## Dynamic partitions

As well as time-based partitions, Dagster also supports dynamic partitions. These  allow for more flexibility. Unlike time-based partitions, dynamic partitions let you control exactly what values are included and grow the partition set as new data categories (like customer names) appear.

Creating a dynamic partition is simple — all you need is a name:

```python
dynamic_partitions_def = dg.DynamicPartitionsDefinition(name="dynamic_partition")
```

This defines a dynamic partition set named "dynamic_partition", which you can configure with whatever partitions we want.

## Dynamic partitioned assets

Similar to our time based partition, let's create a new set of assets. Once again the the logic of our asset will remain the same except it uses the dynamic partition:

```python {% obfuscated="true" %}
# src/dagster_and_etl/defs/assets.py
@dg.asset(
    partitions_def=dynamic_partitions_def,
)
def import_dynamic_partition_file(context: dg.AssetExecutionContext) -> str:
    file_path = (
        Path(__file__).absolute().parent
        / f"../../../data/source/{context.partition_key}.csv"
    )
    return str(file_path.resolve())
```

Now, if we attempted to execute this asset in Dagster, you’d notice that it cannot be materialized. That is because no partitions have been added to `dynamic_partitions_def`. This makes sense as dynamic partitions are empty by default and have no built-in logic to determine which partition keys should exist. It’s up to us to register the partition values we want to execute.

Before we execute the pipeline, let’s define the downstream asset that loads data into DuckDB, using the values from our dynamic partition:

```python {% obfuscated="true" %}
# src/dagster_and_etl/defs/assets.py
@dg.asset(
    kinds={"duckdb"},
    partitions_def=dynamic_partitions_def,
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
            f"delete from {table_name} where date = '{context.partition_key}';"
        )
        conn.execute(f"copy {table_name} from '{import_dynamic_partition_file}';")
```

This setup should look very similar to the daily partition we created earlier. But how does it play out in practice? To better understand the distinction, let’s dive into the differences in how partitioned pipelines are triggered. Each type requires a different approach to scheduling and orchestration, depending on how and when new data becomes available.
