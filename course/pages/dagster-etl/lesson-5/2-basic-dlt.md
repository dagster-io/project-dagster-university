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

Finally, while we’re building a custom API integration here, it's worth noting that dlt also provides out-of-the-box support for [many common verified sources](https://dlthub.com/docs/dlt-ecosystem/verified-sources/).
