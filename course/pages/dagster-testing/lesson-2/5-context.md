---
title: 'Lesson 2: Context'
module: 'dagster_testing'
lesson: '2'
---

In Dagster, assets have a special argument of `context`. This accesses the `AssetExecutionContext` object in Dagster that exposes relevant APIs for systems such as resources, configuration and logging.

Setting the context in an asset is not necessary and if your assets do not access any of the context APIs you will not need to worry about it for testing.

However if we rework the `loaded_file` asset to include context logging, we will need to update our tests. 

```python
@dg.asset()
def loaded_file_logging(context: dg.AssetExecutionContext) -> str:
    current_file_path = os.path.dirname(os.path.realpath(__file__))
    file_name = os.path.join(current_file_path, "path.txt")

    # Includes logging
    context.log.info(f"Reading file {file_name}")

    with open(file_name) as file:
        return file.read()
```

Now when writing the test, the context object is required. This test that worked for our function without logging will now fail:

```python
def test_loaded_file_logging_no_context():
    result = loaded_file_logging()
    assert result == "  contents  "
```

We can set the context object for testing by using the Dagster function `build_asset_context`. Using this function we can set the context parameter:

```python
def test_loaded_file_logging():
    context = dg.build_asset_context()
    result = loaded_file_logging(context)
    assert result == "  contents  "
```

Which will now pass

## Materialize context

Another way to handle context is using `materialize`. We already saw that this executes the assets directly and supplies the necessary run information:

```python
def test_assets_context():
    result = dg.materialize(
        assets=[loaded_file_logging],
    )
    assert result.success

    result.output_for_node("loaded_file_logging") == "  example  "
```

The logging asset will pass even though we do not explicitly pass in the context object and the test will pass.

### Context other uses

There are other situations where we may need to supply context. For example if we have a partitioned asset:

```python
number_partitions = dg.StaticPartitionsDefinition(["1", "2", "3"])


@dg.asset(partitions_def=number_partitions)
def partition_asset_number(context: dg.AssetExecutionContext) -> int:
    return int(context.partition_key)
```

Now we can use the `build_asset_context` to create the context object and set a partition key for testing:

```python
def test_partition_asset_number() -> None:
    context = dg.build_asset_context(partition_key="1")
    assert partition_asset_number(context) == 1
```

We can still use `materialize` to execute our assets that use context, though we will need to set the specific partition:

```python
def test_asssets_partition() -> None:
    result = dg.materialize(
        assets=[
            partition_asset_number,
        ],
        partition_key="1",
    )
    assert result.success

    result.output_for_node("partition_asset_number") == 1
```

One thing to note about materializing multiple partitioned assets. Just like when launching a run in the Dagster UI, you cannot use `materialize` to execute multiple partitioned assets if they do not share the same partition. For example if we try and run this materialization with an additional asset, the test will fail:

```python
@pytest.mark.skip
def test_asssets_multiple_partition() -> None:
    result = dg.materialize(
        assets=[
            partition_asset_number,
            partition_asset_letter,
        ],
        partition_key="1",
    )
    assert result.success

    result.output_for_node("partition_asset_letter") == 1
    result.output_for_node("partition_asset_letter") == "A"
```