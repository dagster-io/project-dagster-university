---
title: "Lesson 4: API Dagster assets"
module: 'dagster_etl'
lesson: '4'
---

# API Dagster assets

Now that we have a better understanding of how we want to structure data extraction from the API, we can start laying out our Dagster code. Since we want the pipeline to be runnable for any given date, a good first step is to create a run configuration (as we did in the previous lesson) that allows us to specify the target date at execution time. This provides the flexibility to manually trigger runs, automate daily ingestion, or even backfill historical data when needed:

```python
class NasaDate(dg.Config):
    date: str
```

Since Dagster run configurations are built on top of Pydantic models, we can use a `field_validator` to ensure the provided date string is in the correct format (e.g., `YYYY-MM-DD`). This adds a layer of validation that helps catch issues early, before the pipeline begins executing:


```python
class NasaDate(dg.Config):
    date: str

    @field_validator("date")
    @classmethod
    def validate_date_format(cls, v):
        try:
            datetime.datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueError("event_date must be in 'YYYY-MM-DD' format")
        return v
```

## Dagster asset

With our run configuration in place, we can now define our Dagster assets. Our first asset will be called `asteroids`, and it will use the `NASAResource` we defined earlier to extract asteroid data for a specific day. In this case, the previous day based on the date provided in the run configuration.

To make the correct API call, we’ll need to compute both the start_date and end_date using that input date. The asset will return a list of dictionaries, each representing an asteroid observed during that time period:

```python {% obfuscated="true" %}
@dg.asset(
    kinds={"nasa"},
    group_name="api_etl",
)
def asteroids(
    context: dg.AssetExecutionContext,
    config: NasaDate,
    nasa: NASAResource,
):
    anchor_date = datetime.datetime.strptime(config.date, "%Y-%m-%d")
    end_date = (anchor_date - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    return nasa.get_near_earth_asteroids(
        start_date=config.date,
        end_date=end_date,
    )
```

Now that we’ve fetched the data from the API, the next step is getting that data into DuckDB. One approach would be to run an `INSERT` statement for each record, but that pattern isn’t ideal for OLAP databases like DuckDB, which are optimized for bulk inserts rather than row-by-row operations.

A more efficient method, and one that aligns with what we did in the previous lesson, is to write the data to a file and then load that file into DuckDB using a `COPY` statement or a similar bulk load mechanism.

So, our next asset will take the list of dictionaries returned by the API and save it to a flat file (e.g., a CSV). To simplify the output and avoid dealing with deeply nested JSON structures, we’ll narrow our focus to just the following fields:

- id
- name
- absolute_magnitude_h
- is_potentially_hazardous_asteroid

```python {% obfuscated="true" %}
@dg.asset(
    group_name="api_etl",
)
def asteroids_file(
    context: dg.AssetExecutionContext,
    asteroids,
) -> Path:
    filename = "asteroid_staging"
    file_path = (
        Path(__file__).absolute().parent / f"../../../../data/staging/{filename}.csv"
    )

    # Only load specific fields
    fields = [
        "id",
        "name",
        "absolute_magnitude_h",
        "is_potentially_hazardous_asteroid",
    ]

    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)

        writer.writeheader()
        for row in asteroids:
            filtered_row = {key: row[key] for key in fields if key in row}
            writer.writerow(filtered_row)

    return file_path
```

The final asset will look very similar to the one we built in the previous lesson. We’ll create a table in DuckDB with the four selected fields and use a `COPY` statement to load the data from the file we just wrote. This approach takes advantage of DuckDB’s efficient bulk loading capabilities and keeps the asset clean and performant. By reusing the same pattern, we maintain consistency across our ETL pipelines, whether the source is a local file or an external API:

```python
@dg.asset(
    kinds={"duckdb"},
    group_name="api_etl",
)
def duckdb_table(
    context: dg.AssetExecutionContext,
    database: DuckDBResource,
    asteroids_file,
) -> None:
    table_name = "raw_asteroid_data"
    with database.get_connection() as conn:
        table_query = f"""
            create table if not exists {table_name} (
                id varchar(10),
                name varchar(100),
                absolute_magnitude_h float,
                is_potentially_hazardous_asteroid boolean
            ) 
        """
        conn.execute(table_query)
        conn.execute(f"COPY {table_name} FROM '{asteroids_file}'")
```

We can now execute the pipeline for a specific date.