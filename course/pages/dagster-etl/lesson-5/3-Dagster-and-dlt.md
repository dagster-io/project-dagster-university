---
title: "Lesson 5: Dagster and dlt"
module: 'dagster_etl'
lesson: '5'
---

# Dagster and dlt

Dagster is built to integrate seamlessly with the best tools in the modern data ecosystem — using each tool where it makes the most sense within your pipeline. That’s why we created specialized integrations for libraries like dlt. This feature is called Embedded ETL, and it's designed to combine the simplicity and flexibility of lightweight ETL frameworks with the robustness and orchestration capabilities of Dagster.

These lightweight services pair well with Dagster because they can leverage Dagster’s existing architecture. Many standalone ETL tools require setting up separate infrastructure — like databases and task queues — to handle state tracking and orchestration. With Dagster, those responsibilities are already built-in. Instead of duplicating that architecture, tools like dlt can integrate directly and let Dagster manage scheduling, retries, observability, and lineage.

![Dagster and dlt](/images/dagster-etl/lesson-5/dlt-etl.png)

## dlt assets

To see this in action, we’ll take the dlt quickstart pipeline we just created and convert it into a set of Dagster assets.

We’ll continue using the `simple_source` function decorated with `@dlt.source`. The only change is that we’ll now inject the `data` list directly within the function, so it behaves as a self-contained data source inside the pipeline:

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

Next, we’ll update our `resources.py` file to include the `DagsterDltResource`. This resource allows Dagster to execute dlt pipelines directly, bridging the gap between Dagster’s orchestration layer and dlt’s data loading capabilities. With this integration in place, we no longer need to define a separate `DuckDBResource` in Dagster — dlt will now be fully responsible for loading data into the database:


```python
import dagster as dg
from dagster_dlt import DagsterDltResource

defs = dg.Definitions(
    resources={
        "dlt": DagsterDltResource(),
    },
)
```

Back in `assets.py`, we can define our dlt assets. This will resemble the dlt.pipeline code we used earlier, but much of the logic will now be embedded in the `@dlt_assets` decorator. The function itself simply yields the result of running the `dlt pipeline`:

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

Just like that, the same dlt pipeline we previously built can now be executed and tracked by Dagster! This integration doesn’t just improve maintainability, it also cleans up our code and reduces boilerplate, making our ETL pipelines more modular and production-ready.

This works well for our simple example, but the real power comes next, we’ll refactor our earlier CSV and API pipelines to use dlt for extraction and loading, while continuing to orchestrate and monitor them through Dagster.
