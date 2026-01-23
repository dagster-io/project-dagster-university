---
title: 'Lesson 6: Asset checks'
module: 'dagster_testing'
lesson: '6'
---

# Asset checks

One key aspect of testing data is validation and data quality. Tests like this are special and have a different work flow than our unit and integration tests. Instead of being run outside of the main application before the code is live, these data validation checks exist in the production environment alongside the assets.

When designing data validation steps, it is best to keep that code separate from the core logic of our assets. This gives us more flexibility on how to handle issues around validation and can help us reuse certain elements.

In order to solve the problem of data quality, Dagster offers asset checks which validate assets when they execute. Asset checks are part of your Dagster project and are set in the definitions like any other Dagster object. When looking in the asset graph you will not see them directly but will see them associated with the asset.

# Defining asset checks

To define an asset check we first need an asset. `total_population` is a slightly modified version of the asset we have used throughout the course. Now it will take in the output of several assets and sums their populations.

```python
# src/dagster_testing/defs/assets/lesson_6.py
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
# src/dagster_testing/defs/assets/lesson_6.py
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
# tests/test_lesson_6.py
def test_non_negative():
    asset_check_pass = lesson_6.non_negative(10)
    assert asset_check_pass.passed
    asset_check_fail = lesson_6.non_negative(-10)
    assert not asset_check_fail.passed
```

```bash
> pytest tests/test_lesson_6.py::test_non_negative
...
tests/test_lesson_6.py .                                                          [100%]
```

# Blocking asset checks

By default, asset checks run alongside asset materialization and report their results. However, you can use `blocking=True` to prevent downstream asset materialization if a check fails. This is useful for critical data quality gates.

```python
@dg.asset_check(asset=raw_data, blocking=True)
def validate_schema(raw_data: list[dict]) -> dg.AssetCheckResult:
    """Block downstream processing if schema is invalid."""
    required_columns = {"id", "name", "email"}
    actual_columns = set(raw_data[0].keys()) if raw_data else set()

    passed = required_columns.issubset(actual_columns)

    return dg.AssetCheckResult(
        passed=passed,
        metadata={
            "required_columns": list(required_columns),
            "actual_columns": list(actual_columns),
        },
    )
```

**When to use blocking checks**:
- Schema validation before transformation
- Critical data quality checks
- Prerequisites for expensive downstream operations

# Asset check severity

Asset checks can report different severity levels to indicate the importance of a failure. Use `dg.AssetCheckSeverity` to distinguish between errors and warnings.

```python
@dg.asset_check(asset=my_data)
def row_count_check(my_data: list) -> dg.AssetCheckResult:
    row_count = len(my_data)
    
    if row_count == 0:
        return dg.AssetCheckResult(
            passed=False,
            severity=dg.AssetCheckSeverity.ERROR,
            metadata={"row_count": 0},
        )
    elif row_count < 100:
        return dg.AssetCheckResult(
            passed=True,  # Warning, not failure
            severity=dg.AssetCheckSeverity.WARN,
            metadata={"row_count": row_count, "message": "Low row count"},
        )
    else:
        return dg.AssetCheckResult(
            passed=True,
            metadata={"row_count": row_count},
        )
```

The `WARN` severity allows you to flag potential issues without failing the check, which is useful for soft thresholds or advisory conditions.

# Multi-asset checks

When you have multiple checks that operate on the same data, loading the asset once and running all checks together is more efficient. Use `@dg.multi_asset_check` for this pattern.

```python
@dg.multi_asset_check(
    specs=[
        dg.AssetCheckSpec(name="unique_ids", asset="customer_data"),
        dg.AssetCheckSpec(name="no_null_emails", asset="customer_data"),
    ]
)
def customer_data_checks(customer_data: list[dict]):
    """Run multiple checks in a single execution."""
    ids = [row["id"] for row in customer_data]
    unique_count = len(set(ids))
    total_count = len(ids)

    yield dg.AssetCheckResult(
        check_name="unique_ids",
        passed=unique_count == total_count,
        metadata={"duplicates": total_count - unique_count},
    )

    null_emails = sum(1 for row in customer_data if row["email"] is None)

    yield dg.AssetCheckResult(
        check_name="no_null_emails",
        passed=null_emails == 0,
        metadata={"null_count": null_emails},
    )
```

**Use `@multi_asset_check` when**:
- Multiple checks run on the same data
- Loading the asset is expensive
- Checks share computation logic

# Factory pattern for asset checks

When you need to apply the same check logic to multiple assets or columns, use a factory function to generate checks programmatically.

```python
def create_not_null_check(asset_name: str, column: str):
    """Factory to create not-null checks for any column."""
    @dg.asset_check(asset=asset_name, name=f"{column}_not_null")
    def check_fn(asset_value: list[dict]) -> dg.AssetCheckResult:
        null_count = sum(1 for row in asset_value if row.get(column) is None)
        return dg.AssetCheckResult(
            passed=null_count == 0,
            metadata={"null_count": null_count, "column": column},
        )
    return check_fn

# Generate checks
email_check = create_not_null_check("customer_data", "email")
name_check = create_not_null_check("customer_data", "name")
```

This pattern reduces code duplication and makes it easy to maintain consistent validation rules across your project.
