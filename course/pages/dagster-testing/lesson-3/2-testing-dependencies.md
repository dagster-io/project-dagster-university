---
title: 'Lesson 3: Testing dependencies'
module: 'dagster_testing'
lesson: '3'
---

# Testing dependencies

Most Dagster asset graphs contain multiple assets that depend on the output of other assets. Linking one asset to another is how you define the structure of your graph. When your assets take in inputs outside of their control, it is important to still configure deterministic tests that will always execute as expected.

We will add an additional asset downstream of `state_population_file` that takes in its output:

```python
# /dagster_testing/defs/assets/lesson_3.py
@dg.asset
def total_population(state_population_file: list[dict]) -> int:
    return sum([int(x["Population"]) for x in state_population_file])
```

The code above defines an asset called `total_population`:

1. Takes in the list of dicts output by the asset `state_population_file`.
2. Returns the total population of all cities in the list.

The relationship of `state_population_file` and `total_population` is defined by the input parameter on `total_population`. What would a test look like for this asset? Click **View answer** to view it.

```python {% obfuscated="true" %}
def test_total_population():
    state_populations = [
        {
            "City": "New York",
            "Population": "8804190",
        },
        {
            "City": "Buffalo",
            "Population": "278349",
        },
        {
            "City": "Yonkers",
            "Population": "211569",
        },
    ]

    assert lesson_3.total_population(state_populations) == 9294108
```

Because we are setting the input parameter for `total_population` we can ensure what the expected outcome will be. In this case the sum of the three cities is 9,294,108.

Like the other asset test, this test looks like standard Python. Again, we can run this test with `pytest`:

```bash
> pytest tests/test_lesson_3.py::test_total_population
...
tests/test_lesson_3.py .                                                          [100%]
```

## Testing materializations

As your pipelines become more complex, it's a good idea to test materializing your Dagster assets. `dg.materialize()` is a `dagster.ExecuteInProcessResult` which will execute assets. We can then check the `success` property of the execution to ensure that everything materialized as expected.

Since the `processed_file` asset only relies on the output of  the `loaded_file` asset, we can materialize both of those assets together to ensure they are working as expected:

```python
def test_assets():
    _assets = [
        lesson_3.state_population_file,
        lesson_3.total_population,
    ]
    result = dg.materialize(_assets)
    assert result.success
```

```bash
> pytest tests/test_lesson_3.py::test_assets
...
tests/test_lesson_3.py .                                                          [100%]
```

Confirming that the assets materialize without issue is a great start, but we still want to check the return values of each asset. Luckily `materialize()` allows us to access the output value with the `output_for_node()` method for each asset from the materialization:

```python
def test_assets():
    _assets = [
        lesson_3.state_population_file,
        lesson_3.total_population,
    ]
    result = dg.materialize(_assets)
    assert result.success

    state_populations = [
        {
            "City": "New York",
            "Population": "8804190",
        },
        {
            "City": "Buffalo",
            "Population": "278349",
        },
        {
            "City": "Yonkers",
            "Population": "211569",
        },
    ]
    assert result.output_for_node("state_population_file") == state_population
    assert result.output_for_node("total_population") == 9294108
```

Using `output_for_node()` we access the individual assets and ensure that their output still matches what we expect.

## Logging

Since we are using Dagster to execute the assets, when we run `materialize()`, the default Dagster event execution will be logged. If you rerun `pytest` with the `-s` flag set to view the logs, all of the Dagster logs will be included as well as the test output:

```bash
> pytest tests/test_lesson_3.py::test_assets -s
...
tests/test_lesson_3.py 2025-02-14 09:30:11 -0600 - dagster - DEBUG - __ephemeral_asset_job__ - 7924f6b8-72c6-4789-b34a-d25b144f7f66 - 62349 - RUN_START - Started execution of run for "__ephemeral_asset_job__".
2025-02-14 09:30:11 -0600 - dagster - DEBUG - __ephemeral_asset_job__ - 7924f6b8-72c6-4789-b34a-d25b144f7f66 - 62349 - ENGINE_EVENT - Executing steps in process (pid: 62349)
2025-02-14 09:30:11 -0600 - dagster - DEBUG - __ephemeral_asset_job__ - 7924f6b8-72c6-4789-b34a-d25b144f7f66 - 62349 - RESOURCE_INIT_STARTED - Starting initialization of resources [io_manager].
...
```

Including the logging can be useful when debugging a broken test and can help you isolate where you are encountering an error.