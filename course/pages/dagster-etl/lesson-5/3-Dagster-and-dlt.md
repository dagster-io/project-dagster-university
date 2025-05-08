---
title: "Lesson 5: Dagster and dlt"
module: 'dagster_etl'
lesson: '5'
---

# Dagster and dlt

Dagster is built around integrating with the best tools in the space and using them where it makes sense in your pipelines. That is why we created speccial integrations for tools like dlt. This feature is called Embedded ETL and is designed to combine lightweight ETL frameworks with the robutness of Dagster.

These lightweight services work so well with Dagster because they can leverage our existing architecture. Other ETL tools tend to rely on databases and queues in order to handle stateful processes and task tracking. These services overlap with Dagster so rather than having to define that architecture separately, dlt and Dagster can work together.

![Dagster and dlt](/images/dagster-etl/lesson-5/dlt-etl.png)

## dlt assets

To see how this works. Let's take the dlt quick start pipeline we just created and turn it into Dagster assets.

We will still need the `dlt.source` decorated `simple_source` function we had defined. The only difference is we will inject the `data` list within the function itself.

```python
@dlt.source
def simple_source():
    @dlt.resource
    def load_dict():
        data = [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"},
        ]

        yield data

    return load_dict
```

Now within the `resources.py` file we will include the `DagsterDltResource`. This resource allows Dagster to both execute dlt pipelines. Note that we no longer need the Dagster `DuckDBResource`. That is because dlt will be reponsible for loading our data.

```python
import dagster as dg
from dagster_dlt import DagsterDltResource

defs = dg.Definitions(
    resources={
        "dlt": DagsterDltResource(),
    },
)
```

Back in `assets.py` we can now define our dlt assets. This will look similar to the dlt `pipeline` code except most of it will be defined in the `@dlt_assets` decorator. The function itself will just yield a run of the dlt pipeline.

```python
@dlt_assets(
    dlt_source=simple_source(),
    dlt_pipeline=dlt.pipeline(
        pipeline_name="simple_pipeline",
        dataset_name="simple",
        destination="duckdb",
        progress="log",
    ),
)
def dlt_assets(context: dg.AssetExecutionContext, dlt: DagsterDltResource):
    yield from dlt.run(context=context)
```

Now that same dlt pipeline we had before can be executed with Dagster! Using Dagster and dlt together not only makes our ETL pipelines more maintainable, but cleans up our code.

This is great for our simple dlt example. Next we will refactor the CSV and API pipelines from the previous sections to use dlt.
