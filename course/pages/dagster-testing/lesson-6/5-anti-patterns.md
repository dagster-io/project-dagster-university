---
title: 'Lesson 6: Anti-patterns to avoid'
module: 'dagster_testing'
lesson: '6'
---

# Anti-patterns to avoid

As you build out your test suite, there are some common mistakes that can reduce the effectiveness of your tests or make them harder to maintain. Here are some anti-patterns to watch out for.

| Anti-Pattern | Better Approach |
| ------------ | --------------- |
| Testing in production | Use staging or mock resources |
| No assertions beyond `success` | Use `output_for_node()` to verify outputs |
| Ignoring test isolation | Each test should be independent |
| Hardcoded test data paths | Use fixtures and relative paths |
| Skipping asset check tests | Test checks like any other function |

## Testing in production

Never run tests against production systems unless you have a read-only, isolated subset. Production testing risks data corruption and may introduce unexpected costs.

**Instead**: Use mock resources for unit tests and staging/Docker environments for integration tests.

## Only checking `success`

A test that only asserts `result.success` doesn't verify that your asset produced the correct output:

```python
# Anti-pattern: Only checks that it ran
def test_my_asset():
    result = dg.materialize(assets=[my_asset])
    assert result.success  # This doesn't test the actual output!
```

**Instead**: Use `output_for_node()` to verify the asset produced the expected result:

```python
# Better: Verify the actual output
def test_my_asset():
    result = dg.materialize(assets=[my_asset])
    assert result.success
    assert result.output_for_node("my_asset") == expected_data
```

## Ignoring test isolation

Tests that depend on shared state or execution order are fragile and difficult to debug.

**Instead**: Each test should be completely independent. Use fixtures to set up test data and tear it down afterward.

## Hardcoded paths

Hardcoding absolute paths makes tests fail when run on different machines or CI environments:

```python
# Anti-pattern: Hardcoded path
def test_data_loading():
    data = load_data("/Users/john/project/data/test.csv")
```

**Instead**: Use relative paths or fixtures:

```python
# Better: Use Path relative to the test file
from pathlib import Path

def test_data_loading():
    test_dir = Path(__file__).parent
    data = load_data(test_dir / "data/test.csv")
```

## Skipping asset check tests

Asset checks contain validation logic that can have bugs just like any other code. Don't assume they work correctly just because they're "simple".

**Instead**: Test your asset checks with both passing and failing inputs:

```python
def test_non_negative_check():
    # Test passing case
    result_pass = non_negative(10)
    assert result_pass.passed
    
    # Test failing case
    result_fail = non_negative(-10)
    assert not result_fail.passed
```

## Summary

Writing good tests is as much about avoiding bad practices as it is about following good ones. Keep your tests focused, isolated, and thorough. When in doubt, ask yourself: "Would this test catch a real bug in my code?" If the answer is no, the test may need improvement.
