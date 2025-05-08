---
title: "Lesson 5: Basic dlt"
module: 'dagster_etl'
lesson: '5'
---

# Basic dlt

When you think about dlt you should consider your source and your destination. To start with our source will be a list of dicts contained in our dlt code and the destination will be the same DuckDB database we have been using.

A basic dlt pipeline would look something like this:

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

load_info = pipeline.run(simple_source())
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

Since dlt is a pure Python framework, there are no other dependencies we need to install.

## dlt Benefits

What should stand out the most with the dlt approach is how much more erognomic it is compared to the code we wrote ourselves. If you remember how we had been working with DuckDB we had to manually program a few steps to load the data:

1. Stage the data (in a csv file).
2. Define the table in DuckDB before loading the data.
3. Load the data into DuckDB with a `COPY` statement.

dlt hides the responsibilty for all of those steps. When we work with dlt all we have to do is define the destination. dlt handles the management of the schema and table (as well as inferring our data types) and loading data.