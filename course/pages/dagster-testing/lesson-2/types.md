---
title: 'Lesson 2: Types'
module: 'dagster_testing'
lesson: '2'
---

In generic Python a function does not need to match its type annotation. For example:

```python
def func_wrong_type() -> str:
    return 2


def test_func_wrong_type():
    assert func_wrong_type() == 2
```

Will still pass even though the function is marked as producing a `str` while an `int` is returned.

Now let's try the same example with Dagster:

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

A benefit of Dagster is that it enforces type checking. This helps improve data quality and the integrity of your pipelines by ensuring the output always matches what is set in the asset.

## Exception handling

While Dagster handles type checking for us. We can still write tests for exceptions in the same way we would any other test. For example:

```python
@dg.asset
def wrong_type_annotation() -> str:
    return 2


def test_wrong_type_annotation_error():
    with pytest.raises(DagsterTypeCheckDidNotPass):
        wrong_type_annotation()
```

However we would not need to write a test like this because this asset would never be able to materialize successfully.