---
title: 'Lesson 6: Asset checks'
module: 'dagster_testing'
lesson: '6'
---

# Asset checks

One key aspect of testing data is validation and data quality. Tests like this are special and have a different work flow than our unit and integration tests. Instead of being run outside of the main application before the code is live, these data validation checks exist in the production environment alongside the assets.

When designing data validation steps, it is best to keep that code separate from the core logic of our assets. This gives us more flexibility on how to handle issues around validation and can help us reuse certain elements.

In order to solve the problem of data quality, Dagster offers asset checks which validate assets when they execute. Asset checks are part of your Dagster project and are set in the definitions like any other Dagster object. When looking in the asset graph you will not see them directly but will see them associated with the asset.

![Asset checks](/images/dagster-testing/lesson-6/asset-check.png)

When the asset runs, we can see that its associated asset checks also run and validate.

![Asset checks success](/images/dagster-testing/lesson-6/asset-check-success.png)

# Defining asset checks

To define an asset check we first need an asset. `total_population` is a slightly modified version of the asset we have used throughout the course. Now it will take in the output of several assets and sums their populations.

```python
# /dagster_testing/assets/dagster_assets.py
@dg.asset
def total_population(
    state_population_file_config: list[dict],
    state_population_api_resource: list[dict],
) -> int:
    all_assets = state_population_file_config + state_population_api_resource
    return sum([int(x["Population"]) for x in all_assets])
```

Say we wanted to write a test to ensure that the number returned by `total_population` is always positive. We would define an asset check using the `dg.asset _check` decorator. Within the decorator we link it to the `total_population`.

```python
@dg.asset_check(asset=total_population)
```

Now `total_population` can be used an input parameter for the function itself. This is what the asset check might look like. Click **View answer** to view it.

```python {% obfuscated="true" %}
@dg.asset_check(asset=total_population)
def non_negative(total_population):
    return dg.AssetCheckResult(
        passed=bool(total_population > 0),
    )
```

The function itself checks if the result of `total_population` is above 0 and sets that result to `AssetCheckResult` which will be stored within the Dagster metadata history.

# Tests for asset checks

You can also write unit tests for your asset check code. Depending on the level of complexity contained within your asset checks it can be helpful to have tests to ensure assets are properly validated.

Writing a test for our asset check is similar to writing a test for an asset. Our input parameter is the value we wish to check and then we can see if the asset did or did not pass validation.

```python
def test_non_negative():
    asset_check_pass = dagster_assets.non_negative(10)
    assert asset_check_pass.passed
    asset_check_fail = dagster_assets.non_negative(-10)
    assert not asset_check_fail.passed
```

```bash
> pytest dagster_testing_tests/test_lesson_6.py::test_non_negative
...
dagster_testing_tests/test_lesson_6.py .                                                          [100%]
```
