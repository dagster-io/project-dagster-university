---
title: "Lesson 5: Refactoring static data with dlt"
module: 'dagster_etl'
lesson: '5'
---

# Refactoring static data with dlt

There are a couple of key differences between our original CSV pipeline and the dlt quickstart we just converted into Dagster assets. First, the CSV pipeline uses a run configuration to allow a specific file name to be passed in at runtime. Second, the dlt asset in this case is dependent on an upstream asset that stages the file.

We’ll start by reusing the existing run configuration and upstream asset, both of which can remain unchanged. This allows us to maintain the same flexible file-based interface while swapping in dlt to handle the data loading:

```python
# src/dagster_and_etl/defs/assets.py
class FilePath(dg.Config):
    path: str


@dg.asset
def import_file(context: dg.AssetExecutionContext, config: FilePath) -> str:
    file_path = (
        Path(__file__).absolute().parent / f"../../../data/source/{config.path}"
    )
    return str(file_path.resolve())
```

Next, we need to define the `dlt.source` function for our CSV pipeline. This will look very similar to the `simple_source` function we used earlier, but with a few changes: it will read from a CSV file and take a file path as an input parameter. This allows us to dynamically pass in the file we want to process, while letting dlt handle the parsing and schema inference:

```python {% obfuscated="true" %}
@dlt.source
def csv_source(file_path: str = None):
    def load_csv():
        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            data = [row for row in reader]

        yield data

    return load_csv
```

This is very helpful. Before our pipelines had to be hardcoded to define the schema for the destination table. Offloading your schema management to a framework can make your pipelines much less error prone. Though it is still good to be aware of what data types it has selected. Just because a zip code looks like an integer does not mean that is how we want the data represented.

So far, things are looking very similar to our previous setup. We’ll once again use the `@dlt_assets `decorator to generate our dlt-backed assets. The one key difference in this case is that our `csv_source` function accepts an input parameter for the file path.

Just like in our earlier Dagster pipeline, this parameter will be satisfied by the upstream `import_file` asset. This allows the dlt asset to consume the file path dynamically and run the ETL process based on the specific file returned by `import_file`:

```python {% obfuscated="true" %}
@dlt_assets(
    dlt_source=csv_source(),
    dlt_pipeline=dlt.pipeline(
        pipeline_name="csv_pipeline",
        dataset_name="csv_data",
        destination="duckdb",
        progress="log",
    ),
)
def dlt_csv_assets(
    context: dg.AssetExecutionContext, dlt: DagsterDltResource, import_file
):
    yield from dlt.run(context=context, dlt_source=csv_source(import_file))
```

## dlt Translator

This setup might look complete, but there’s one final step we need to take. Because dlt assets are generated differently, they also have a unique way of handling dependencies.

If you’ve taken the [Dagster & dbt course](https://courses.dagster.io/courses/dagster-dbt), you may recall the need for a Translator to map dbt assets to other assets in your Dagster project. Similarly, for dlt, we use a specialized translator — the `DagsterDltTranslator` — to accomplish the same thing.

In this case, we want to map our dlt asset to depend on the import_file asset, so that the file path returned by import_file is passed into the dlt source function. Fortunately, this is straightforward to implement. Our translator will look like this:


```python
class CustomDagsterDltTranslator(DagsterDltTranslator):
    def get_asset_spec(self, data: DltResourceTranslatorData) -> dg.AssetSpec:
        default_spec = super().get_asset_spec(data)
        return default_spec.replace_attributes(
            deps=[dg.AssetKey("import_file")],
        )
```

With the translator set. We can include it within the `dlt_assets` decorator for the `dagster_dlt_translator` parameter:

```python
@dlt_assets(
    ...
    dagster_dlt_translator=CustomDagsterDltTranslator(),
)
```
