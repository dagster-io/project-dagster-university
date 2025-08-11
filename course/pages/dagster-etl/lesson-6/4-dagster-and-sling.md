---
title: "Lesson 6: Dagster and Sling"
module: 'dagster_etl'
lesson: '6'
---

# Dagster and Sling

When defining assets with Sling, you will first have to define your source and target. In this case our source is Postgres and the destination is still our DuckDB database.

To define the source and destination, we will use the `SlingConnectionResource`. The source POstgres instance will use the connection details from our Docker Compose.

```python
# src/dagster_and_etl/defs/resources.py
import dagster as dg
from dagster_sling import SlingConnectionResource, SlingResource

source = SlingConnectionResource(
    name="MY_POSTGRES",
    type="postgres",
    host="localhost",
    port=5432,
    database="test_db",
    user="test_user",
    password="test_pass",
)
```

The destination has fewer attributes as it is just the file path to our local DuckDB database:

```python
# src/dagster_and_etl/defs/resources.py
destination = SlingConnectionResource(
    name="MY_DUCKDB",
    type="duckdb",
    connection_string="duckdb:///var/tmp/duckdb.db",
)
```

With the source and destination defined, we can combine them together in the `SlingResource` and set it within the `dg.Definitions`:

```python
# src/dagster_and_etl/definitions.py
defs = dg.Definitions(
    resources={
        "sling": sling,
    },
)
```

## Replication yaml

Our connections are set but we still need to set what we are replicating. Sling handles this with a replication yaml file. This determines which connection is our source and target:

```yaml
source: MY_POSTGRES
target: MY_DUCKDB
```

More importantly we need to decide which of our tables to replicate between Postgres and DuckDB. We only need the `data.customers`, `data.products` and `data.orders` tables so can set those in the `streams`.

```yaml
defaults:
  mode: full-refresh

  object: "{stream_schema}_{stream_table}"

streams:
  data.customers:
  data.products:
  data.orders:
```

This will replicate our 3 tables into DuckDB.

## Sling assets

Now we can generate our Dagster assets. Since we have already done most of the work in defining our source and destination in the `SlingResource` and the replication information in the `replication.yaml`, Dagster can automatically generate the assets with the `sling_assets` decorator:


```python
# src/dagster_and_etl/defs/assets.py
import dagster as dg
from dagster_sling import SlingResource, sling_assets

replication_config = dg.file_relative_path(__file__, "sling_replication.yaml")


@sling_assets(replication_config=replication_config)
def postgres_sling_assets(context, sling: SlingResource):
    yield from sling.replicate(context=context).fetch_column_metadata()
```

That is everything we need. Now when we launch `dg dev` we will see six new assets in the asset graph.

First there are the three source assets representing the raw tables that exist in our Postgres database (customers, products, orders). Connected to each of these sources are our Dagster assets. Each of these individually.