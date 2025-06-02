---
title: "Lesson 5: Refactoring apis with dlt"
module: 'dagster_etl'
lesson: '5'
---

# Refactoring APIs with dlt

Next we can reconfigure our API pipeline with dlt. This is a much more custom implementation than loading data from a CSV so the `@dlt.source` will contain more code. However, we can simply reuse most of the logic from the previous lesson.

```python
@dlt.source
def nasa_neo_source(start_date: str, end_date: str, api_key: str):
    @dlt.resource
    def fetch_neo_data():
        url = "https://api.nasa.gov/neo/rest/v1/feed"
        params = {
            "start_date": start_date,
            "end_date": end_date,
            "api_key": api_key,
        }

        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()

        for neo in data["near_earth_objects"][start_date]:
            neo_data = {
                "id": neo["id"],
                "name": neo["name"],
                "absolute_magnitude_h": neo["absolute_magnitude_h"],
                "is_potentially_hazardous": neo["is_potentially_hazardous_asteroid"],
            }

            yield neo_data

    return fetch_neo_data
```

This gives us the ability to pull in any date range from the NASA api using dlt. Rather than using the `dlt_assets` decorator. We can also nest this code directly in a dg asset. We can then update the `nasa_neo_source` function to use the values from the run configuration.

```python
@dg.asset
def dlt_nasa(context: dg.AssetExecutionContext, config: NasaDate):
    anchor_date = datetime.datetime.strptime(config.date, "%Y-%m-%d")
    start_date = (anchor_date - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    @dlt.source
    def nasa_neo_source():
        @dlt.resource
        def load_neo_data():
            url = "https://api.nasa.gov/neo/rest/v1/feed"
            params = {
                "start_date": start_date,
                "end_date": config.date,
                "api_key": os.getenv("NASA_API_KEY"),
            }

            response = requests.get(url, params=params)
            response.raise_for_status()

            data = response.json()

            for neo in data["near_earth_objects"][config.date]:
                neo_data = {
                    "id": neo["id"],
                    "name": neo["name"],
                    "absolute_magnitude_h": neo["absolute_magnitude_h"],
                    "is_potentially_hazardous": neo[
                        "is_potentially_hazardous_asteroid"
                    ],
                }

                yield neo_data

        return load_neo_data

    pipeline = dlt.pipeline(
        pipeline_name="nasa_neo_pipeline",
        destination=dlt.destinations.duckdb(os.getenv("DUCKDB_DATABASE")),
        dataset_name="nasa_neo",
    )

    load_info = pipeline.run(nasa_neo_source())

    return load_info
```

Writing the function this way also makes it easy to include partitions as we would for any other asset.

```python
@dg.asset(
    partitions_def=nasa_partitions_def,
    automation_condition=dg.AutomationCondition.on_cron("@daily"),
)
def dlt_nasa_partition(context: dg.AssetExecutionContext):
    anchor_date = datetime.datetime.strptime(context.partition_key, "%Y-%m-%d")
    start_date = (anchor_date - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    @dlt.source
    def nasa_neo_source():
        @dlt.resource
        def load_neo_data():
            url = "https://api.nasa.gov/neo/rest/v1/feed"
            params = {
                "start_date": start_date,
                "end_date": context.partition_key,
                "api_key": os.getenv("NASA_API_KEY"),
            }

            response = requests.get(url, params=params)
            response.raise_for_status()

            data = response.json()

            for neo in data["near_earth_objects"][context.partition_key]:
                neo_data = {
                    "id": neo["id"],
                    "name": neo["name"],
                    "absolute_magnitude_h": neo["absolute_magnitude_h"],
                    "is_potentially_hazardous": neo[
                        "is_potentially_hazardous_asteroid"
                    ],
                }

                yield neo_data

        return load_neo_data

    pipeline = dlt.pipeline(
        pipeline_name="nasa_neo_pipeline",
        destination=dlt.destinations.duckdb(os.getenv("DUCKDB_DATABASE")),
        dataset_name="nasa_neo",
    )

    load_info = pipeline.run(nasa_neo_source())

    return load_info
```
