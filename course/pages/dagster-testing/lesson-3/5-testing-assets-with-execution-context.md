---
title: 'Lesson 3: Testing assets with execution context'
module: 'dagster_testing'
lesson: '3'
---

# Testing assets with execution context

In Dagster, assets can optionally take a special argument of `context`. This argument accesses the `AssetExecutionContext` object in Dagster that exposes relevant APIs for systems such as resources, configuration, and logging.

If your assets do not access any of the context APIs, you will not need to worry about `context` for testing.

However if we rewrite the `state_population_file` asset to include context logging, we will need to update our tests:

```python
# /dagster_testing/defs/assets/lesson_3.py
@dg.asset()
def state_population_file_logging(context: dg.AssetExecutionContext) -> list[dict]:
    file_path = Path(__file__).absolute().parent / "../data/ny.csv"

    context.log.info(f"Reading file {file_path}")

    with open(file_path) as file:
        reader = csv.DictReader(file)
        return [row for row in reader]
```

Now when we write a test for this asset, it must include the context object. The following test that worked for our asset that did not include `context` will now fail:

```python
def test_state_population_file_logging_no_context(file_output):
    result = lesson_3.state_population_file_logging()
    assert result == file_output
```

We can set the context object for testing by using the Dagster function `build_asset_context`. Using this function, we can set the `context` parameter:

```python
def test_state_population_file_logging(file_output):
    context = dg.build_asset_context()
    result = lesson_3.state_population_file_logging(context)
    assert result == file_output
```

The test above should now pass.

```bash
> pytest tests/test_lesson_3.py::test_state_population_file_logging
...
tests/test_lesson_3.py .                                                          [100%]
```

## Handling context with materialize()

You can also handle context with `materialize()`. We already saw that this executes the assets directly and supplies the necessary run information:

```python
def test_assets_context(file_output):
    result = dg.materialize(
        assets=[lesson_3.state_population_file_logging],
    )
    assert result.success

    assert result.output_for_node("state_population_file_logging") == file_output
```

When using `dg.Materialize()`, context does not need to be explicitly passed in.

### Supplying context for partitioned assets

Another situations where we may need to supply context is when testing partitioned asset. We will rewrite the `state_population_file` asset once again into a partitioned asset. We will define three different static partitions for the asset for each of the state files that exists in the `data` directory:

```python
file_partitions = dg.StaticPartitionsDefinition(["ca.csv", "mn.csv", "ny.csv"])


@dg.asset(partitions_def=file_partitions)
def state_population_file_partition(context: dg.AssetExecutionContext) -> list[dict]:
    file_path = Path(__file__).absolute().parent / f"../data/{context.partition_key}"
    with open(file_path) as file:
        reader = csv.DictReader(file)
        return [row for row in reader]
```

Now in order to execute this asset we need to provide one of the three partitions. We can use `build_asset_context()` to create the context object and set a partition key for testing:

```python
def test_state_population_file_partition(file_output):
    context = dg.build_asset_context(partition_key="ny.csv")
    assert lesson_3.state_population_file_partition(context) == file_output
```

```bash
> pytest tests/test_lesson_3.py::test_state_population_file_partition
...
tests/test_lesson_3.py .                                                          [100%]
```

We can still use `materialize()` to execute our assets that use context, though we will need to set the specific partition:

```python
def test_assets_partition(file_output):
    result = dg.materialize(
        assets=[
            lesson_3.state_population_file_partition,
        ],
        partition_key="ny.csv",
    )
    assert result.success

    assert result.output_for_node("state_population_file_partition") == file_output
```

```bash
> pytest tests/test_lesson_3.py::test_assets_partition
...
tests/test_lesson_3.py .                                                          [100%]
```

It's important to remember that when materializing multiple partitioned assets, just like when launching a run in the Dagster UI, you cannot use `materialize()` to execute multiple partitioned assets if they do not share the same partition. For example, if we try to run the following materialization with an additional asset, the test will fail:

```python
def test_assets_multiple_partition() -> None:
    result = dg.materialize(
        assets=[
            lesson_3.state_population_file_partition,
            lesson_3.partition_asset_letter,
        ],
        partition_key="ny.csv",
    )
    assert result.success

    result.output_for_node("state_population_file_partition") == 1
    result.output_for_node("partition_asset_letter") == "A"
```