---
title: 'Lesson 5: Asset checks'
module: 'dagster_testing'
lesson: '5'
---

One key aspect of testing data is validation. Tests like this are special and have a different work flow than our unit and integration tests. Instead of being run outside of the main application before the code is live, these data validation checks exist in the production environment and are run as our assets are executing.

Generally we want this code to exist separately from the core logic of our assets to keep things more maintainable. To solve this problem, Dagster offers asset checks which validate assets when they execute. Asset checks are part of your Dagster project and are set in the definitions like any other Dagster object. When looking in the asset graph you will not see them directly but will see them associated with their asset.

![Asset checks](/images/dagster-essentials/lesson-5/asset-check.png)

When the asset runs, we can see that its asset check also validates.

![Asset checks success](/images/dagster-essentials/lesson-5/asset-check-success.png)

# Defining asset checks

To define an asset check we first need an asset. `combine_asset` takes in the output of several other assets and sums their values:

```python
@dg.asset
def combine_asset(config_asset: int, resource_asset: int) -> int:
    return config_asset + resource_asset
```

Say we wanted to write a test for this asset to ensure that number returned is positive. What would that look like?

```python {% obfuscated="true" %}
@dg.asset_check(asset=combine_asset)
def non_negative(combine_asset):
    return dg.AssetCheckResult(
        passed=bool(combine_asset > 0),
    )
```

The `asset_check` decorator associates the function with the `combine_asset` asset. We will also provide that asset as a parameter in the asset check function because we want to test the output. The function itself checks if the result of combine_asset is above 0 and sets that result to the `AssetCheckResult`.

# Tests for asset checks

You can also write unit tests for your asset checks. Depending on the level of complexity contained within your asset checks it can be helpful to have tests to ensure assets are properly validated:

```python
def test_non_negative():
    asset_check_pass = assets.non_negative(10)
    assert asset_check_pass.passed
    asset_check_fail = assets.non_negative(-10)
    assert not asset_check_fail.passed
```

Writing a test for our asset check is similar to writing a test for an asset. Our input parameter is the value we wish to check and then we can see if the asset did or did not pass validation.