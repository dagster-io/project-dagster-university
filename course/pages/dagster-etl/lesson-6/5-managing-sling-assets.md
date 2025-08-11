---
title: "Lesson 6: Executing the pipeline"
module: 'dagster_etl'
lesson: '6'
---

# Executing the pipeline

We’ve defined all the assets we need, but we haven’t yet discussed how we want to execute this pipeline. When running data replication in production, there are a few important considerations to keep in mind.

## Triggering our job

First, let’s consider the best way to trigger our ETL assets. While some ETL tools, like Debezium, support continuous data loading, most are schedule-based.

Choosing the right schedule can be nuanced. Depending on how the data is extracted (which we’ll cover later), running schedules too frequently may be inefficient. For example, if you attempt to run a job multiple times per minute, one execution might not finish before the next one starts—this can lead to a backup and degraded performance.

On the other hand, if your schedules are too far apart, you risk missing timely updates and working with stale data. In practice, running your schedules a few times per day, based on data volume and business needs, is often a good balance.

Creating a schedule for our Sling ETL assets is no different than defining any other schedule in Dagster. Suppose we want to run two schedules:

* One that refreshes all Sling assets once a day
* Another that refreshes the orders asset three times a day

We’d define two separate jobs:

```python
# src/dagster_and_etl/defs/jobs.py
import dagster as dg

postgres_refresh_job = dg.define_asset_job(
    "postgres_refresh",
    selection=[
        dg.AssetKey(["target", "data", "customers"]),
        dg.AssetKey(["target", "data", "products"]),
        dg.AssetKey(["target", "data", "orders"]),
    ],
)

orders_refresh_job = dg.define_asset_job(
    "orders_refresh",
    selection=[
        dg.AssetKey(["target", "data", "orders"]),
    ],
)
```

Then we can create two distinct schedules with different cron expressions:

```python
# src/dagster_and_etl/defs/schedules.py
postgres_refresh_schedule = dg.ScheduleDefinition(
    job=postgres_refresh_job,
    cron_schedule="0 6 * * *",
)

orders_refresh_schedule = dg.ScheduleDefinition(
    job=orders_refresh_job,
    cron_schedule="0 12,18 * * *",
)
```

With these schedules in place, all ETL assets will refresh at 6 UTC, and the orders asset will additionally refresh at 12 and 18 UTC.

## Replication Strategies

We haven’t yet discussed how data is replicated with Sling. If you’ve looked at the `replication.yaml` file, you may have noticed that the default mode is set to `full-refresh`:

```yaml
defaults:
  mode: full-refresh
```

This is the same as the full refresh strategy we discussed about earlier where the entire table is copied over every time. For the small database we’re using, this is fine. However, as data volumes grow, you may want to switch to a more efficient replication strategy.

Sling does not offer a full CDC solution but we can still manage replication with fairly large databases by using incremental replication.

Let’s think about our schema. Of the three tables, customers, products, and orders, which is most likely to grow the largest? The orders table. This makes sense: a single user may place many orders, and each order can involve multiple products.

Another important characteristic of the orders table is the presence of a time-based column, order_date, which tracks when an order was created. We can use this column to filter the records we need to process during each run.

To do this, we can configure the `replication.yaml` file to make orders an incremental asset, using the order_date column to track changes:

```yaml
  data.orders:
    mode: incremental
    primary_key: order_id
    update_key: order_date
```

With this configuration, Sling will only process new or updated records based on the order_date, reducing data load and improving performance.

Incremental replication is just one of [many strategies supported by Sling](https://docs.slingdata.io/examples/database-to-database). Regardless of the tool you use, it's important to select a replication approach that fits your data's characteristics and your system's requirements.
