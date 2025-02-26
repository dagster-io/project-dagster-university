---
title: 'Lesson 3: Testing asset output types'
module: 'dagster_testing'
lesson: '2'
---

# Testing asset output types

In standard Python, a function does not need to match its type annotation in order to execute properly. For example:

```python
def func_wrong_type() -> str:
    return 2


def test_func_wrong_type():
    assert func_wrong_type() == 2
```

The test above will pass even though the function is marked as producing a `str` while an `int` is returned.

A benefit of Dagster is that it enforces type checking when you annotate the function attached to an asset. This helps improve data quality and the integrity of your pipelines by ensuring the output always matches its expected type.


Let's try the same example with Dagster:

```python
@dg.asset
def wrong_type_annotation() -> str:
    return 2


def test_wrong_type_annotation():
    assert wrong_type_annotation() == 2
```

Will this pass? Click **View answer** to view it.

```bash {% obfuscated="true" %}
> pytest dagster_testing_tests/test_lesson_2.py::test_wrong_type_annotation
...
dagster_testing_tests/test_lesson_2.py F                        [100%]
...
E           dagster._core.errors.DagsterTypeCheckDidNotPass: Type check failed for op "wrong_type_annotation" output "result" - expected type "String". Description: Value "2" of python type "int" must be a string.
...
FAILED dagster_testing_tests/test_lesson_2.py::test_wrong_type_annotation - dagster._core.errors.DagsterTypeCheckDidNotPass: Type check failed...
```

Because Dagster enforces types as part of its execution, we will never need to write a tests around type check. Just make sure that your annotate any assets where you care about types.

## Exception handling

While we will not need to write tests to ensure our data types, it can be beneficial to write tests that catch exceptions. For example if we wanted to make sure our asset fails correct when it cannot connect to a database or we have exceeded the rate limit for an API.

With `pytest`, handling exceptions within Dagster is the same as exception handling with other standard Python functions. If we wanted to write a test to ensure that the `wrong_type_annotation` asset would raise an error, it would look like this:

```python
@dg.asset
def wrong_type_annotation() -> str:
    return 2


def test_wrong_type_annotation_error():
    with pytest.raises(DagsterTypeCheckDidNotPass):
        wrong_type_annotation()
```