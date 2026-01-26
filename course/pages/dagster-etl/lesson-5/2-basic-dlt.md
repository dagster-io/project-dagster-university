---
title: "Lesson 5: Basic dlt"
module: 'dagster_etl'
lesson: '5'
---

# Basic dlt

When working with dlt, you should think in terms of two main components: your source and your destination. In our case, the source will be a simple list of dictionaries defined in our code, and the destination will be the same DuckDB database we’ve been using throughout this course.

This setup allows us to explore the basics of how a dlt pipeline works without adding complexity. Once you're comfortable with the mechanics, you can easily scale up to dynamic sources like APIs or cloud storage.

```python
import os

import dlt

data = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
]


@dlt.source
def simple_source():
    @dlt.resource
    def load_dict():
        yield data

    return load_dict


pipeline = dlt.pipeline(
    pipeline_name="simple_pipeline",
    destination=dlt.destinations.duckdb(os.getenv("DUCKDB_DATABASE")),
    dataset_name="mydata",
)

load_info = pipeline.run(simple_source(), write_disposition="replace")
```

The code above does the following:

1. Creates a list containing two dicts called `data`.
2. Uses the `dlt.source` decorator to define a source function, inside of this source is a `dlt.resource` decorated function that yields the list defined above.
3. Creates a pipeline using `dlt.pipeline()` that sets the pipeline name, destination (DuckDB) and name of the dataset as it will appear in DuckDB.
4. Executes the pipeline with `pipeline.run`.

We can execute this code by running the file:

```bash
python dlt_quick_start.py
```

Since dlt is a pure Python framework, there are no additional services or heavy dependencies required, it runs natively in your Python environment.

## dlt Benefits

What stands out most about the dlt approach is how much more ergonomic and streamlined it is compared to the code we previously wrote by hand. Recall that when working directly with DuckDB, we had to manually manage several tedious steps:

* Stage the data by writing it to a CSV file.
* Define the target table and schema in DuckDB ahead of time.
* Load the data using a COPY statement.

With dlt, all of these responsibilities are abstracted away. Once you define your destination, dlt takes care of the rest. Its configuration based approach to REST APIs minimizes the amount of code required, reducing it to just the configuration object.

In addition to simplifying setup, dlt handles a number of complex API behaviors out of the box, including:

* Pagination
* Chained/multi-step API requests
* Other common API reliability issues

dlt also takes care of:

* Schema and table creation
* Data type inference
* Loading the data into your destination

This dramatically reduces boilerplate code and makes your ETL pipelines more maintainable, reliable, and adaptable.

Finally, while we're building a custom API integration here, it's worth noting that dlt also provides out-of-the-box support for [many common verified sources](https://dlthub.com/docs/dlt-ecosystem/verified-sources/).

## Write Dispositions in Practice

In our simple example above, we used `write_disposition="replace"`. Let's understand when to use each option:

```python
# Replace: Good for dimension tables or full refreshes
load_info = pipeline.run(simple_source(), write_disposition="replace")

# Append: Good for event logs or fact tables
load_info = pipeline.run(simple_source(), write_disposition="append")

# Merge: Good for upserts based on primary key
load_info = pipeline.run(
    simple_source(),
    write_disposition="merge",
    primary_key="id"
)
```

The `merge` disposition is particularly powerful for maintaining data integrity. When you specify a `primary_key`, dlt will update existing records if they match, and insert new ones if they don't. This is essential for maintaining accurate, deduplicated data.

## Incremental Loading

For sources that continuously produce new data (like APIs or event streams), you don't want to reload everything on each run. dlt supports incremental loading using the `dlt.sources.incremental` helper:

```python
@dlt.resource
def load_events(
    last_timestamp=dlt.sources.incremental("timestamp", initial_value="2024-01-01")
):
    # Only fetch records newer than last_timestamp.last_value
    for event in fetch_events_since(last_timestamp.last_value):
        yield event
```

dlt automatically tracks the highest value seen for the incremental column and stores it in pipeline state. On the next run, it will only process records with values greater than the stored state.

## State Management

dlt manages pipeline state automatically in a `_dlt_pipeline_state` table in your destination. This state includes:

- Last values for incremental columns
- Schema versions and migrations
- Load package metadata

This means you can safely restart pipelines, and they'll pick up right where they left off—no manual bookkeeping required.

## Error Handling and Troubleshooting

When things go wrong, dlt provides helpful tools for debugging:

### Viewing Load Information

The `load_info` object returned by `pipeline.run()` contains detailed information about what happened:

```python
load_info = pipeline.run(source)

# Check for errors
if load_info.has_failed_jobs:
    for job in load_info.load_packages[0].jobs["failed_jobs"]:
        print(f"Failed: {job.file_path}, Error: {job.failed_message}")

# View load statistics
print(load_info)  # Prints a summary of loaded tables and row counts
```

### Common Issues

| Problem | Likely Cause | Solution |
|---------|--------------|----------|
| Duplicate records | Wrong write_disposition | Use `merge` with `primary_key` |
| Missing recent data | State not advancing | Check `_dlt_pipeline_state` table |
| Schema errors | Incompatible type changes | Use `replace` disposition for clean reload |
| Memory issues | Large batch sizes | Use generators (`yield`) instead of lists |

### Resetting Pipeline State

If you need to start fresh, you can reset the pipeline state:

```python
pipeline = dlt.pipeline(pipeline_name="my_pipeline", destination="duckdb")
pipeline.drop()  # Removes all state and destination tables
```

{% callout type="warning" title="State Reset Warning" %}
Dropping pipeline state will cause the next run to reload all data from scratch. For incremental sources, this may result in duplicate processing if you're using `append` mode.
{% /callout %}
