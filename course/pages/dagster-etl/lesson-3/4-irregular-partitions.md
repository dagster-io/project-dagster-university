---
title: "Lesson 3: Irregular partitions"
module: 'dagster_etl'
lesson: '3'
---

## Irregular partitions

So far we have looked at partitioning data from sources that follow specific patterns. Files that are associated with specific times (daily, weekly, monthly) work well with partitions and are easy to track.

But what about those cases that do not follow a specific pattern. What if the upstream data sources produce data based on some other criteria like by customer names. Something like customer name may change over time as new customers are added but we want to still ensure they all fall under the same partitions.

## Dynamic Partitions

In Dagster you can create dynamic partitions which represent more flexible partitions, where you manage what is represented within the partition. Creating a dynamic partition is simple, all it requires is a name:

```python
s3_partitions_def = dg.DynamicPartitionsDefinition(name="s3")
```

We can then create a new asset that is the same as our other partitioned asset except it uses the dynamic partition.

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

If you wanted to execute this asset in Dagster you would see that in order to materialize, you need to add a partition. This makes sense because our dynamic partition has no logic associated with it and therefore has no idea what partitions should be included.

Let's add another downstream associate to load data in DuckDB associated with the dynamic partition.

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

This should all look very similar to the daily partition we set before. So how does this play out in practice? To better understand that distinction we will dive into the differences in how we can trigger these different pipelines.