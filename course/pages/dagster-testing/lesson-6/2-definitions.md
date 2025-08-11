---
title: 'Lesson 6: Definitions'
module: 'dagster_testing'
lesson: '6'
---

# Definitions

Within your Dagster project the most important object is the `Definitions`. This defines all the objects that will deployed into your code location. If you are using `dg` you may already be in the habit of checking to ensure your `Definitions` is valid by running `dg check defs`.

This is a great habit and you can build out workflows (such as precommit hooks) to always run that check. But it is also good to get in the habit of writing a specific test for this to live alongside your other Dagster tests.

Luckily this is a very easy test to write.

## Loading the Definition object

The `@dg.definitions` decorator is lazily evaluated. This means it is not loaded until it is needed. In order to load the definition we can use the `load_defs` function.

We can now write a test to assert that the definition can load properly.

```python
# tests/test_lesson_6.py
import dagster_testing.defs

def test_defs():
    assert dg.Definitions.merge(dg.components.load_defs(dagster_testing.defs))
```

```bash
> pytest tests/test_lesson_6.py::test_def
...
tests/test_lesson_6.py .                                                          [100%]
```

As simple as it may seem, this test will find many issues associated with your Dagster project. This ensures that all the Dagster objects can load successfully and that certain dependencies between objects are satisfied (such a given resource being present if it is required for an asset). So if there is an issue loading any of your assets, asset checks, jobs, resources, schedules and sensors into the definition this test will trigger.

We can also pull out loading the definition into a fixture if we want to run multiple tests against the definition.

```python
# tests/test_lesson_6.py
@pytest.fixture()
def defs():
    return dg.Definitions.merge(dg.components.load_defs(dagster_testing.defs))

def test_defs(defs):
    assert defs
```

{% callout %}

💡 **Unit tests:** While this test will catch many issues, we still need individual tests to ensure that the assets and other Dagster objects __execute__ as expected. The definition test only ensures proper __loading__ of the objects.

{% /callout %}

## Definition objects

The `Definitions` object includes additional methods for access various objects contained withi. For example rather than importing assets directly, you can access them from the definitions object. For example we can access the `squared` asset and test it from the definitions.

```python
# tests/test_lesson_6.py
def test_square_asset(defs):
    _asset = defs.get_assets_def("squared")
    assert _asset(5) == 25
```

```bash
> pytest tests/test_lesson_6.py::test_square_asset
...
tests/test_lesson_6.py .                                                          [100%]
```

Be aware that access Dagster objects is different when they have named keys. For example the asset `squared_key`.

```python
# src/dagster_testing/defs/assets/lesson_6.py
@dg.asset(key=["target", "main", "square_key"])
def squared_key(number: int):
    return number * number
```

In order to access this asset you must set the key with `dg.AssetKey`.

```python
# tests/test_lesson_6.py
def test_square_key_asset(defs):
    _asset = defs.get_assets_def(dg.AssetKey(["target", "main", "square_key"]))
    assert _asset(5) == 25
```

## Components

Accessing Dagster objects from the `definitions` object is especially useful when working with components.

Since components typically do not expose their underlying Dagster objects as directly importable code, you should load the `definitions` object and access the relevant objects from it when writing tests or performing operations involving component-generated assets or jobs.

```python
# tests/test_lesson_6.py
def test_materialize_partition(defs, duckdb_resource):
    result = dg.materialize(
        assets=[
            defs.get_assets_def(dg.AssetKey(["target", "main", "stg_customers"])), # asset from dbt component
            defs.get_assets_def(dg.AssetKey(["target", "main", "stg_orders"])), # asset from dbt component
            defs.get_assets_def(dg.AssetKey(["target", "main", "stg_payments"])), # asset from dbt component
            assets.monthly_orders, # user defined component downstream of dbt
        ],
        resources={
            "duckdb": duckdb_resource,
        },
        partition_key="2024-01-01",
    )
    assert result.success
```