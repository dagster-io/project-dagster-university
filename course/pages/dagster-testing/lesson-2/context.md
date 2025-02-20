---
title: 'Lesson 2: Context'
module: 'dagster_testing'
lesson: '2'
---

In Dagster assets there is a special optional argument of `context`. This accesses the `AssetExecutionContext` object in Dagster that exposes relevant APIs for systems such as resources, configuration and logging. If your asset does not use this context you will not need to worry about it for testing. But what if you wanted to add logging to the `loaded_file` asset? 

```python {% obfuscated="true" %}
@dg.asset()
def loaded_file_logging(context: dg.AssetExecutionContext) -> str:
    current_file_path = os.path.dirname(os.path.realpath(__file__))
    file_name = os.path.join(current_file_path, "path.txt")

    context.log.info(f"Reading file {file_name}")

    with open(file_name) as file:
        return file.read()
```

Now when writing the test, the context object is required. For example this test will fail:

```python
def test_loaded_file_logging_no_context():
    result = loaded_file_logging()
    assert result == "  contents  "
```

We can get around this by using the Dagster function `build_asset_context` to build the context and supply it to the function:

```python
def test_loaded_file_logging():
    context = dg.build_asset_context()
    result = loaded_file_logging(context)
    assert result == "  contents  "
```

Another way to handle context is using `materialize`. We already saw that this executes the assets directly and supplies the necessary run information:

```python
def test_assets_context():
    result = dg.materialize(
        assets=[loaded_file_logging],
    )
    assert result.success

    result.output_for_node("loaded_file_logging") == "  example  "
```

### Context other uses

There are other situations where we may need to supply context. For example if we have a partitioned asset:

```python
number_partitions = dg.StaticPartitionsDefinition(["1", "2", "3"])


@dg.asset(partitions_def=number_partitions)
def partition_asset_number(context: dg.AssetExecutionContext) -> int:
    return int(context.partition_key)
```

Now we can use the `build_asset_context` to create the context object and supply a partition key for testing:

```python
def test_partition_asset_number() -> None:
    context = dg.build_asset_context(partition_key="1")
    assert partition_asset_number(context) == 1
```

We can still use `materialize` to execute our assets, though we will still need to set the specific partition:

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

However you should note. Just like if you were to use the Dagster UI to launch a run, you cannot use `materialize` to execute multiple partitioned assets if they do not share the same partition. This test will fail:

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