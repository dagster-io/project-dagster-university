---
title: "Lesson 4: API resource"
module: 'dagster_etl'
lesson: '4'
---

# API Resource

When working with external APIs with Dagster, it is usually best to first create a resource. Creating a resource will give us a nice abstraction that we can use across multiple assets to interact with the API. It will also make testing and maintaining our pipelines much easier.

Before we start writing any code, let's look at the characteristics of the NeoWs API. The base URL for this endpoint is `https://api.nasa.gov/neo/rest/v1/feed` which has three parameters associated with it.

| Parameter	| Type | Default | Description|
| --- | --- | --- | --- |
| start_date | YYYY-MM-DD | none | Starting date for asteroid search |
| end_date | YYYY-MM-DD | 7 days after start_date | Ending date for asteroid search |
| api_key | string | DEMO_KEY | api.nasa.gov key for expanded usage |

This means that a full API request would look like:

`https://api.nasa.gov/neo/rest/v1/feed?start_date=2015-09-07&end_date=2015-09-08&api_key=DEMO_KEY`

This will return a large JSON object. To keep things easy, we can ignore most of the metadata in the JSON. We are interested in getting the information about asteroids. So from this JSON we are interested in the "near_earth_objects" field for the date we are parsing.

## Coding our resource

We know the API endpoint and the parameters necessary to make an API call. Let's start writing out our resource. There are many ways to write this but we want a resource named `NASAResource` that is initialized with an API key and has a single method `get_near_earth_asteroids` that takes in two parameters: `start_date` and `end_date` which will return our JSON.

```python {% obfuscated="true" %}
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
        return resp.json()["near_earth_objects"][start_date]
```

Now that we have our resource defined, we can include it in the `Definitions` alongside the `DuckDBResource`.

```python
defs = dg.Definitions(
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

Remember you will need to set the environment variable `NASA_API_KEY` to the API key you created if you want to execute this pipeline.