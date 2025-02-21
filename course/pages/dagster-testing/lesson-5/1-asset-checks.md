---
title: 'Lesson 5: Asset checks'
module: 'dagster_testing'
lesson: '5'
---

One aspect of testing that is key in data is validation. As well as ensuring that everything runs without error, we need to be sure to assess the quality of the data. Tests like this are special and need to exist live in the production environment as data is flowing. To accomplish this Dagster offers asset checks which are tests that verify specific properties of your data assets, allowing you to execute data quality checks on your data.

Asset checks are associated with the assets themselves. So we will start with an asset `combine_asset` that takes in several other assets and combines their values:

```python
@dg.asset
def combine_asset(config_asset: int, resource_asset: int, partition_asset: int) -> int:
    return config_asset + resource_asset + partition_asset
```

Say we wanted to write a test for `combine_asset` to ensure that number returned is positive. What would that look like?

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