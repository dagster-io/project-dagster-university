---
title: 'Lesson 2: Dependencies'
module: 'dagster_testing'
lesson: '2'
---

Most likely your assets do not exist in isolation but are downstream of other assets. Let's add another asset that takes a dependency on the `loaded_file` asset:

```python
@dg.asset
def processed_file(loaded_file: str) -> str:
    return loaded_file.strip()
```

The code above:

1. Takes in content returned by the `loaded_file` asset
2. Returns that contents stripped of whitespace as a `str`


The only difference from the `loaded_file` asset is that `processed_file` takes in an argument which is the string returned by `loaded_file`. Think of what a test may look like. Click **View answer** to view it.

```python {% obfuscated="true" %}
def test_processed_file():
    assert processed_file(" contents  ") == "contents"
```

Like before you do not need to do anything special. Writing a unit test for this asset behaves like a regular Python function.

```bash
> pytest dagster_testing_tests/test_lesson_2.py::test_processed_file
...
dagster_testing_tests/test_lesson_2.py .                                                          [100%]
```

## Testing materializations

As your pipelines get more complex, it can be helpful to also run tests by running your assets the way Dagster would materialize them.

Since `loaded_file` is completely hardcoded and `processed_file` only relies on the output of `loaded_file` we can materialize both of those assets together to ensure they are working as expected.

```python
def test_assets():
    assets = [
        loaded_file,
        processed_file,
    ]
    result = dg.materialize(assets)
    assert result.success
```

```bash
> pytest dagster_testing_tests/test_lesson_2.py::test_assets
...
dagster_testing_tests/test_lesson_2.py .                                                          [100%]
```

This is a great start since we know the assets materialize without issue but we may still want to check the return values of each asset. Luckily `materialize` allows us to access the output value for all the assets.

```python
def test_assets():
    assets = [
        loaded_file,
        processed_file,
    ]
    result = dg.materialize(assets)
    assert result.success

    result.output_for_node("loaded_file") == "  contents  "
    result.output_for_node("processed_file") == "contents"
```

Using `output_for_node` we access the individual assets and ensure that everything is still behaving as expected.

## Logging

One thing to note about using `materialize`. Since we are using Dagster to execute the assets, the default event execution will be logged as well. If you rerun `pytest` with the `-s` flag set to view the logs, all of the Dagster logs will be included as well:

```bash
> pytest dagster_testing_tests/test_lesson_2.py::test_assets -s
...
dagster_testing_tests/test_lesson_2.py 2025-02-14 09:30:11 -0600 - dagster - DEBUG - __ephemeral_asset_job__ - 7924f6b8-72c6-4789-b34a-d25b144f7f66 - 62349 - RUN_START - Started execution of run for "__ephemeral_asset_job__".
2025-02-14 09:30:11 -0600 - dagster - DEBUG - __ephemeral_asset_job__ - 7924f6b8-72c6-4789-b34a-d25b144f7f66 - 62349 - ENGINE_EVENT - Executing steps in process (pid: 62349)
2025-02-14 09:30:11 -0600 - dagster - DEBUG - __ephemeral_asset_job__ - 7924f6b8-72c6-4789-b34a-d25b144f7f66 - 62349 - RESOURCE_INIT_STARTED - Starting initialization of resources [io_manager].
...
```