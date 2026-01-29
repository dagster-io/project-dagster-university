---
title: 'Lesson 5: Smoke tests'
module: 'dagster_testing'
lesson: '5'
---

# Smoke tests

While integration tests validate that your code works with real systems, there's another powerful technique for catching errors early: **smoke tests**.

## What are smoke tests?

A smoke test runs all your data transformations on empty or synthetic data to catch "stupid mistakes" quickly. These are the kinds of errors that are trivial to fix but hard to spot with the naked eye:

- Trying to access a column that doesn't exist
- Calling a function that doesn't exist or with wrong arguments
- Type mismatches (e.g., performing arithmetic on a string)
- Missing imports or typos in variable names

The key insight is that **you write the smoke test once, and it automatically covers every transformation in your pipeline**. When you add new assets, they're included in the smoke test without writing additional test code.

## Smoke tests vs other test types

| Test Type | Speed | What It Catches | Setup Required |
| --------- | ----- | --------------- | -------------- |
| Unit tests | Very fast | Business logic errors | Mock inputs |
| Smoke tests | Fast | Structural errors | Column schemas |
| Integration tests | Slow | System interaction issues | Real infrastructure |

Smoke tests fill the gap between unit tests and integration tests. They run faster than integration tests (no real I/O) but exercise more of your pipeline than individual unit tests.

## Implementing smoke tests

The strategy is to:

1. Define column schemas for your source assets
2. Create an IO manager that generates empty DataFrames from those schemas
3. Run all assets in-memory using `dg.materialize()`

### Step 1: Define column schemas

For assets that depend on external data sources, add `TableSchema` metadata to describe the expected columns:

```python
import dagster as dg

raw_country_populations = dg.SourceAsset(
    key="raw_country_populations",
    metadata={
        "column_schema": dg.TableSchema.from_name_type_dict(
            {
                "country": "string",
                "continent": "string",
                "pop2023": "int64",
                "pop2024": "int64",
                "change": "float64",
            }
        ),
    },
)
```

This metadata serves double duty: it documents your data for stakeholders in the Dagster UI, and it enables automatic mock data generation for testing.

### Step 2: Create a smoke test IO manager

The `SmokeIOManager` extends `InMemoryIOManager` to handle source assets by generating empty DataFrames with the correct schema:

```python
from dagster import InMemoryIOManager
from pandas import DataFrame, Series

def empty_dataframe_from_schema(column_schema):
    """Create an empty DataFrame with the specified column types."""
    return DataFrame(
        {col.name: Series(dtype=col.type) for col in column_schema.columns}
    )


class SmokeIOManager(InMemoryIOManager):
    """IO manager that generates empty DataFrames for source assets."""

    def load_input(self, context):
        # Check if this input has column_schema metadata
        if context.upstream_output is not None:
            column_schema = context.upstream_output.metadata.get("column_schema")
            if column_schema:
                return empty_dataframe_from_schema(column_schema)

        # For assets without schema metadata, use default in-memory storage
        return super().load_input(context)
```

When loading an input, the IO manager checks if the upstream output has `column_schema` metadata. If it does, it generates an empty DataFrame with those columns. Otherwise, it falls back to the default in-memory behavior.

### Step 3: Run the smoke test

With the IO manager in place, you can run your assets with a single test:

```python
import dagster as dg
import pytest
from dagster_testing.defs.assets import lesson_5

@pytest.mark.smoke
def test_smoke_pipeline():
    result = dg.materialize(
        assets=[
            lesson_5.raw_country_populations,
            lesson_5.country_populations,
            lesson_5.continent_stats,
        ],
        resources={"io_manager": lesson_5.SmokeIOManager()},
    )

    assert result.success
```

This test exercises every transformation in your pipeline with empty data. If any asset has a typo, references a missing column, or has a type error, the test will fail immediately.

The key point is that **you're testing your actual pipeline code**, not test-specific assets. When you add new assets that depend on source assets with `column_schema` metadata, they're automatically covered by the smoke test.

## What smoke tests catch

Smoke tests are particularly effective at catching:

```python
# Missing column access
df["nonexistent_column"]  # ❌ Caught by smoke test

# Wrong function name
df.group_by("col")  # ❌ Should be groupby()

# Type errors
df["price"] + "dollars"  # ❌ Can't add string to numeric

# Missing imports
result = pd.merge(...)  # ❌ If pd not imported
```

## What smoke tests don't catch

Smoke tests verify structure, not correctness. They won't catch:

- Wrong business logic (e.g., multiplying instead of dividing)
- Edge cases with specific data values
- Performance issues
- Data quality problems

For these, you still need unit tests with meaningful test data and integration tests with real systems.

## Smoke tests for SQL pipelines

If your pipeline includes SQL transformations (e.g., dbt models), you'll need a test database. The approach is similar to integration tests, but you populate it with empty tables matching your source schemas:

```python
@pytest.fixture(scope="session")
def smoke_database(docker_postgres):
    """Create empty tables for smoke testing SQL transformations."""
    with docker_postgres.get_connection() as conn:
        for source_asset in source_assets:
            columns = ", ".join(
                f"{col.name} {col.type}"
                for col in source_asset.metadata["column_schema"].columns
            )
            conn.execute(f"""
                CREATE TABLE IF NOT EXISTS {source_asset.key.path[-1]} 
                ({columns})
            """)
    return docker_postgres
```

## Best practices

1. **Run smoke tests in CI**: They're fast enough to run on every commit
2. **Add schema metadata to all source assets**: This documents your data and enables smoke testing
3. **Don't skip smoke tests for "simple" assets**: Even simple transformations can have typos
4. **Combine with other test types**: Smoke tests complement, not replace, unit and integration tests

## Summary

Smoke tests provide a low-effort, high-value testing layer that catches structural errors across your entire pipeline. By defining column schemas on source assets and using a custom IO manager, you can validate that all your transformations will at least run without errors—catching the "stupid mistakes" that waste debugging time.
