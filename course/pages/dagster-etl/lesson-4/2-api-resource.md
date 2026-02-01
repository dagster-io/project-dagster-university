---
title: "Lesson 4: API resource"
module: 'dagster_etl'
lesson: '4'
---

# API Resource

When working with external APIs in Dagster, it's often best to start by creating a resource. A resource provides a clean abstraction for external services, making it easy to reuse API logic across multiple assets. It also simplifies testing and long-term maintenance by isolating API-specific logic in a single, well-defined interface.

Before we write any code, let’s review the characteristics of the NeoWs (Near Earth Object Web Service) API. The base URL for the endpoint is:

```bash
https://api.nasa.gov/neo/rest/v1/feed
```

This endpoint supports three query parameters:

| Parameter	| Type | Default | Description|
| --- | --- | --- | --- |
| start_date | YYYY-MM-DD | none | Starting date for asteroid search |
| end_date | YYYY-MM-DD | 7 days after start_date | Ending date for asteroid search |
| api_key | string | DEMO_KEY | api.nasa.gov key for expanded usage |

Given this structure, a full API request might look like:

```bash
https://api.nasa.gov/neo/rest/v1/feed?start_date=2015-09-07&end_date=2015-09-08&api_key=DEMO_KEY
```

The API will return a large JSON response that includes various metadata fields. To keep things simple, we’ll focus only on the part we care about, the `near_earth_objects` field. This field contains the actual asteroid data, organized by date, and is all we need for our ETL pipeline.

## Coding our resource

Now that we know the API endpoint and the parameters required to make a call, let’s write our resource. There are many ways to structure this, but we’ll keep the implementation lean.

We’ll create a resource called `NASAResource`, which is initialized from our API key. This resource will expose a single method: `get_near_earth_asteroids` with two parameters (start_date, end_date), which returns the parsed JSON response from the API.

Here’s what that might look like added to the `resources.py`:

```python {% obfuscated="true" %}
# src/dagster_and_etl/defs/assets.py
import dagster as dg
import requests


class NASAResource(dg.ConfigurableResource):
    api_key: str

    def get_near_earth_asteroids(self, start_date: str, end_date: str):
        url = "https://api.nasa.gov/neo/rest/v1/feed"
        params = {
            "start_date": start_date,
            "end_date": end_date,
            "api_key": self.api_key,
        }

        resp = requests.get(url, params=params)
        resp.raise_for_status()  # Raises exception for 4xx/5xx errors
        return resp.json()["near_earth_objects"][start_date]
```

{% callout type="note" title="Production Error Handling" %}
In production, you'd want more robust error handling:

```python
import time
from requests.exceptions import RequestException

def get_near_earth_asteroids(self, start_date: str, end_date: str, retries: int = 3):
    for attempt in range(retries):
        try:
            resp = requests.get(url, params=params, timeout=30)
            resp.raise_for_status()
            return resp.json()["near_earth_objects"][start_date]
        except RequestException as e:
            if attempt == retries - 1:
                raise
            time.sleep(2 ** attempt)  # Exponential backoff
```

This handles timeouts, rate limiting (429 errors), and transient failures with exponential backoff.
{% /callout %}

Now that we have our resource defined, we can include it in the `Definitions` alongside the `DuckDBResource` resource in the `resources.py`:

```python
# src/dagster_and_etl/definitions.py
@dg.definitions
def resources():
    return dg.Definitions(
        resources={
            "nasa": NASAResource(
                api_key=dg.EnvVar("NASA_API_KEY"),
            ),
            "database": DuckDBResource(
                database="data/staging/data.duckdb",
            ),
        },
    )
```

**Note**: Remember you will need to set the environment variable `NASA_API_KEY` to the API key you created if you want to execute this pipeline.