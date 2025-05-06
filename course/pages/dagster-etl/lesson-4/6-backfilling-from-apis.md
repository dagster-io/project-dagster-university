---
title: "Lesson 4: Backfilling from APIs"
module: 'dagster_etl'
lesson: '4'
---

# Backfilling from APIs

The ETL API is now set up to bring in all data going forward. But what about previous data? The NASA data actually goes back years and maybe we want to ingest all of it into our data warehouse. What would be the best stratedgy for that?

We can actually use a Dagster feature we used before, partitions. If we partition our data by date we can use Dagster to launch a backfill job to ingest data for specific date ranges. This is a much more elegant solution than doing this through scripting or launching one giant run by pinging and paging through a large time range from the API.

To start let's create a daily partition.

```python
nasa_partitions_def = dg.DailyPartitionsDefinition(
    start_date="2025-04-01",
)
```

Next we can update the `asteroids` asset to use a partition instead of a run configuration. We will create a separate asset for this.


```python {% obfuscated="true" %}
@dg.asset(
    kinds={"nasa"},
    group_name="api_etl",
    partitions_def=nasa_partitions_def,
)
def asteroids_partition(
    context: dg.AssetExecutionContext,
    nasa: NASAResource,
) -> list[dict]:
    anchor_date = datetime.datetime.strptime(context.partition_key, "%Y-%m-%d")
    start_date = (anchor_date - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    return nasa.get_near_earth_asteroids(
        start_date=start_date,
        end_date=context.partition_key,
    )
```

All of the other downstream assets would remain the same so we will keep this as a single asset just to demonstrate what it would look like to implement this with partitions.

## Rate limits

Another reason why partitions are an ideal way to handle backfilling with APIs is because of rate limiting. Especially for APIs that return large amounts of data there is usually some mechanism in place to ensure you do not overwhelm the underlying system.

Partitions do not get around the problem of rate limiting but make it much easier to track which partitions have been ingested. And because partitions are processed individually, there is less of a risk if we hit a rate limit midway through the process.