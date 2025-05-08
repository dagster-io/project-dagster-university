---
title: "Lesson 4: API Dagster assets"
module: 'dagster_etl'
lesson: '4'
---

# API Dagster assets

Now that we know more how we want to structure our data extraction from the API, we can start to lay out our code in Dagster. We want to be able to run the pipeline for any date so we can begin by creating a run configuration for a specific date

```python
class NasaDate(dg.Config):
    date: str
```

Because run configurations inherit from Pydantic, we can also include a `field_validator` to ensure the string is in the correct format.

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

With our run configuration we can now create our Dagster assets. Our first asset should be named `asteroids` and extract the previous day using the `NASAResource` resource we defined earlier. This will return a list of dicts.

Remember that we will also need to set a start and end date for the API call based on the date provided in the run configuration.

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

Now that we have the data from the API, we have to figure out how to get that data into DuckDB. One way to do this would be running an `INSERT` statement and loading all the values. However, most OLAP databases are not optimized for this type of workflow. It is usually much more efficient to load bulk in as files. Similar to how we loaded data in the previous lesson. So our next asset should take in the list of dicts and save them to a file.

Also to keep things easier and avoid some of the nesting that exists in the JSON returned by the API. Let's say we only care about the following fields:

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

The final asset can look very similar to the asset used in the previous lesson. In DuckDB we will create a table (with the four fields mentioned above) and execute a `COPY` statement to load the data.

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