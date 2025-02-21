---
title: 'Lesson 2: Types'
module: 'dagster_testing'
lesson: '2'
---

In standard Python a function does not need to match its type annotation in order to execute properly. For example:

```python
def func_wrong_type() -> str:
    return 2


def test_func_wrong_type():
    assert func_wrong_type() == 2
```

Will pass even though the function is marked as producing a `str` while an `int` is returned.

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

A benefit of Dagster is that it enforces type checking when set in assets. This helps improve data quality and the integrity of the pipelines by ensuring the output always matches its expected type.

## Exception handling

Handling exceptions within Dagster is the same as other functions with pytest. Though it is not necessary, if we wanted to write a test to ensure that this asset would raise an error, it would look like this:

```python
@dg.asset
def wrong_type_annotation() -> str:
    return 2


def test_wrong_type_annotation_error():
    with pytest.raises(DagsterTypeCheckDidNotPass):
        wrong_type_annotation()
```

While testing for exceptions can be beneficial, you will not need to write tests to ensure type. This is much better served by including type annotations.