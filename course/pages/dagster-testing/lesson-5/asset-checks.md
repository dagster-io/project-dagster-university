---
title: 'Lesson 5: Asset checks'
module: 'dagster_testing'
lesson: '5'
---



```python
@dg.asset
def combine_asset(config_asset: int, resource_asset: int, partition_asset: int) -> int:
    return config_asset + resource_asset + partition_asset
```

Say we wanted to write a test for `combine_asset` to ensure that number returned is positive. What would that look like:

```python {% obfuscated="true" %}
@dg.asset_check(asset=combine_asset)
def non_negative(combine_asset):
    return dg.AssetCheckResult(
        passed=bool(combine_asset > 0),
    )
```

# Tests for asset checks

You can also write tests for your asset checks. Depending on the level of complexity of your asset checks. Have tests for your checks can help ensure that your data quality standards are configured how you expect:

```python
def test_non_negative():
    asset_check_pass = assets.non_negative(10)
    assert asset_check_pass.passed
    asset_check_fail = assets.non_negative(-10)
    assert not asset_check_fail.passed
```