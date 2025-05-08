---
title: "Lesson 5: Refactoring static data with dlt"
module: 'dagster_etl'
lesson: '5'
---

# Refactoring static data with dlt

There are a couple of differences between our CSV pipeline and the dlt quickstart we just converted into assets. First of all it has a run configuration so you can supply a file name to process and dlt asset is dependent on an upstream asset.

We can start with the run configuration and asset. These all can actually remain the same:

```python
class FilePath(dg.Config):
    path: str


@dg.asset
def import_file(context: dg.AssetExecutionContext, config: FilePath) -> str:
    file_path = (
        Path(__file__).absolute().parent / f"../../../../data/source/{config.path}"
    )
    return str(file_path.resolve())
```

The next thing we need to do is define the `dlt.source` function. This will look very similar to the `simple_source` function except that it reads from a csv file and takes an input parameter of a file type.

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

So far things are looking pretty much the same. We will use the `dlt_assets` decorator to once again generate dlt assets. The one difference we have to account for is that the `csv_source` function has an input parameter. Like our Dagster pipeline before that parameter is the file path returned from the `import_file` asset.

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

This might look complete but there is actually one final step we need to do. Because the dlt assets are special in how they are generated, they also have a special way to map depdendencies.

If you have taken the [Dagster & dbt course](https://courses.dagster.io/courses/dagster-dbt) you may remember the need for a `Translator` to map our dbt assets to other assets. There is a specific `DagsterDltTranslator` we will use to accomplish the same thing.

In this case we want to map our dlt assets to the `import_file` asset. This is relatively easy and our translator will look like this:


```python
class CustomDagsterDltTranslator(DagsterDltTranslator):
    def get_asset_spec(self, data: DltResourceTranslatorData) -> dg.AssetSpec:
        default_spec = super().get_asset_spec(data)
        return default_spec.replace_attributes(
            deps=[dg.AssetKey("import_file")],
        )
```

With the translator set. We can include it within the `dlt_assets` decorator for the `dagster_dlt_translator` parameter.

```python
@dlt_assets(
    ...
    dagster_dlt_translator=CustomDagsterDltTranslator(),
)
```

