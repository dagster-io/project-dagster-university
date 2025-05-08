---
title: "Lesson 6: dlt database assets"
module: 'dagster_etl'
lesson: '6'
---

# dlt database assets

Because there’s no custom code required, this is one of the simplest dlt asset setups in Dagster. The only source we need is sql_database, which can be imported with:

```python
from dlt.sources.sql_database import sql_database
```

The asset replication code is straightforward:

```python {% obfuscated="true" %}
@dlt_assets(
    dlt_source=sql_database(),
    dlt_pipeline=dlt.pipeline(
        pipeline_name="postgres_pipeline",
        destination="postgres",
        dataset_name="postgres_data",
    ),
)
def dlt_postgres_assets(context: dg.AssetExecutionContext, dlt: DagsterDltResource):
    yield from dlt.run(context=context, dlt_source=sql_database())
```

## Source filtering

It might be surprising how little information dlt needs to get started but that’s thanks to the standardized metadata available in SQL databases. Metadata about schemas, tables, and data types allows dlt to automatically discover what’s available to replicate without requiring manual definitions.

By default, `sql_database` will bring in all tables from the source database. If needed, you can customize this behavior to replicate only a subset of tables. For example:

```python
source = sql_database(table_names=['orders', 'customers'])
```

This can also be set in the `config.toml` file in the `.dlt` directory:

```yaml
[sources.sql_database]
table_names = [
    "orders",
    "customers",  
]
```

## Table-level lineage

This approach gives us table-level asset tracking rather than treating the Postgres database as a single, monolithic source. That’s a major benefit as your schema grows: you can clearly link downstream assets (like models or reports) to the specific source table they depend on, not just the overall replication process.

# TODO - UI screenshot

This level of granularity makes it much easier to understand which tables power which applications, and how changes in one area might affect others — especially as your data platform scales.
