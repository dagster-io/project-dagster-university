---
title: 'Lesson 2: Unit tests'
module: 'dagster_testing'
lesson: '2'
---

# Unit tests

Unit tests are small, isolated tests that check individual pieces of code (usually functions or methods). They focus on testing one unit of functionality at a time, ensuring that each component behaves correctly in isolation.

* Catch Bugs Early – Identify issues before they become bigger problems.
* Ensure Code Reliability – Helps maintain functionality when making changes.
* Improve Refactoring Confidence – You can safely modify code knowing tests will catch regressions.
* Continuous Integration (CI) – Automated tests speed up development and deployment.
* Documentation – Since unit tests are tied directly to the code itself, they can serve as a great form of documentation.

Unit tests in Python generally focus on a single function and ensure it works as expected:

```python
def my_func():
   return 5


def test_my_func():
   assert my_func() == 5
```

### Asset tests

Unit testing works well when thinking in terms of Dagster assets. An asset is responsible for one aspect or node in the overall graph. So by writing unit tests for our asset we can ensure that that isolated node is working as expected.

We will begin with the following asset:

```python
@dg.asset
def loaded_file() -> str:
   current_file_path = os.path.dirname(os.path.realpath(__file__))
   file_name = os.path.join(current_file_path, "path.txt")
   with open(file_name) as file:
       return file.read()
```

The code above:

1. Determines the file path of `path.txt` relative to itself
2. Loads that file
3. Returns the contents of that file as a `str`

The `path.txt` file contains a single line of text "  contents  " (the extra whitespace is intended). To test the behavior of our asset, what would a test look like? Click **View answer** to view it.

```python {% obfuscated="true" %}
def test_loaded_file():
   assert loaded_file() == "  contents  "
```

This is the same as writing a test for a standard Python function. We can use `pytest` for this specific test to ensure everything works as intended:

```bash
> pytest dagster_testing_tests/test_lesson_2.py::test_loaded_file
...
dagster_testing_tests/test_lesson_2.py .                                                          [100%]
```