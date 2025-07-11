---
title: "Lesson 4: Backfilling from APIs"
module: 'dagster_etl'
lesson: '4'
---

# Backfilling from APIs

Our ETL pipeline is now set up to ingest new data from the API on an ongoing basis. But what about historical data? The NASA dataset goes back several years, and we may want to load that full history into our data warehouse.

The best strategy for this is to use a Dagster feature we’ve already worked with: partitions. By partitioning the data by date, we can use Dagster’s built-in backfill functionality to launch jobs that process data across specific date ranges. This is a far more elegant and manageable approach than writing custom scripts or triggering a massive, monolithic run that pages through years of API results.

To begin, let’s define a daily partition for our asteroid ingestion pipeline. This will allow us to backfill one day at a time and track progress across the full history:

```python
nasa_partitions_def = dg.DailyPartitionsDefinition(
    start_date="2025-04-01",
)
```

Next we can update the `asteroids` asset to use a partition instead of a run configuration. We will create a separate asset for this.


```python {% obfuscated="true" %}
@dg.asset(
    kinds={"nasa"},
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

All of the downstream assets we've already built can remain unchanged, so for this example, we’ll focus on a single partitioned asset to demonstrate how backfilling works with partitions.

## Rate limits

Another reason partitions are well-suited for API-based backfills is because of rate limiting. APIs, especially those that return large volumes of data, often enforce limits to prevent excessive load on their systems.

While partitions don't eliminate rate limits, they make it much easier to track progress and recover gracefully. Since each partition represents a discrete time window (like a single day), if a request fails due to a rate limit, only that partition is affected. This avoids losing the entire job and allows you to retry just the failed partitions, rather than restarting the entire ingestion process. It also makes it easy to throttle or space out runs as needed.

If we wanted to include rate limiting functionality into our `NASAResource` what might it look like?

```python {% obfuscated="true" %}
import dagster as dg
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class NASAResource(dg.ConfigurableResource):
    api_key: str

    def get_near_earth_asteroids(self, start_date: str, end_date: str):
        url = "https://api.nasa.gov/neo/rest/v1/feed"
        params = {
            "start_date": start_date,
            "end_date": end_date,
            "api_key": self.api_key,
        }

        # Retries
        session = requests.Session()
        retries = Retry(
            total=5,
            backoff_factor=0.5,
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["GET"]
        )
        adapter = HTTPAdapter(max_retries=retries)
        session.mount("https://", adapter)

        resp = session.get(url, params=params)
        return resp.json()["near_earth_objects"][start_date]
```
