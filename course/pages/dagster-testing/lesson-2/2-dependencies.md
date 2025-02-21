---
title: 'Lesson 2: Dependencies'
module: 'dagster_testing'
lesson: '2'
---

When working with assets it is unlikely that they entirely live in isolation. Your Dagster asset graph is made up of the interplay of all the various assets you define and likely takes in outputs from other assets.

We will add an additional asset downstream of `loaded_file` that takes in its output:

```python
@dg.asset
def processed_file(loaded_file: str) -> str:
    return loaded_file.strip()
```

The code above:

1. Takes in the string returned by `loaded_file`
2. Returns the string stripped of whitespace

The relationship of `loaded_file` and `processed_file` is defined by the input parameter. What would a test look like for this asset? Click **View answer** to view it.

```python {% obfuscated="true" %}
def test_processed_file():
    assert processed_file(" contents  ") == "contents"
```

Like the other asset, nothing about this test looks different from standard Python. Again we can run this test with pytest.

```bash
> pytest dagster_testing_tests/test_lesson_2.py::test_processed_file
...
dagster_testing_tests/test_lesson_2.py .                                                          [100%]
```

## Testing materializations

As your pipelines become more complex and start to contain multiple assets, it can be helpful to also run tests by running your assets as a Dagster materialization.

Since `processed_file` only relies on the output of `loaded_file` we can materialize both of those assets together to ensure they are working as expected.

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

This is a great start since we know the assets materialize without issue but we still want to check the return values of each asset. Luckily `materialize` allows us to access the output value for all the assets from the materialization.

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

Using `output_for_node` we access the individual assets and ensure that their output still matches what we expect.

## Logging

One thing to note about using `materialize`. Since we are using Dagster to execute the assets, the default Dagster event execution will be logged. If you rerun `pytest` with the `-s` flag set to view the logs, all of the Dagster logs will be included as well as the test output:

```bash
> pytest dagster_testing_tests/test_lesson_2.py::test_assets -s
...
dagster_testing_tests/test_lesson_2.py 2025-02-14 09:30:11 -0600 - dagster - DEBUG - __ephemeral_asset_job__ - 7924f6b8-72c6-4789-b34a-d25b144f7f66 - 62349 - RUN_START - Started execution of run for "__ephemeral_asset_job__".
2025-02-14 09:30:11 -0600 - dagster - DEBUG - __ephemeral_asset_job__ - 7924f6b8-72c6-4789-b34a-d25b144f7f66 - 62349 - ENGINE_EVENT - Executing steps in process (pid: 62349)
2025-02-14 09:30:11 -0600 - dagster - DEBUG - __ephemeral_asset_job__ - 7924f6b8-72c6-4789-b34a-d25b144f7f66 - 62349 - RESOURCE_INIT_STARTED - Starting initialization of resources [io_manager].
...
```