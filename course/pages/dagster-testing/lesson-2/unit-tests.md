---
title: 'Lesson 2: Unit tests'
module: 'dagster_testing'
lesson: '2'
---

# Unit tests

Unit tests are small, isolated tests that check whether individual pieces of code (usually functions or methods) work as expected. They focus on testing one unit of functionality at a time, ensuring that each component behaves correctly in isolation.

* Catch Bugs Early – Identify issues before they become bigger problems.
* Ensure Code Reliability – Helps maintain functionality when making changes.
* Improve Refactoring Confidence – You can safely modify code knowing tests will catch regressions.
* Continuous Integration (CI) – Automated tests speed up development and deployment.
* Documentation – Since unit tests are tied directly to the code itself, they can serve as a great form of documentation.

### Asset tests

Unit testing works well when thinking in terms of assets. Since an asset is responsible for one aspect of compute, we can ensure it is behaving as expected. We can start with a completely isolated asset:

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

Luckily testing an asset is not any different from testing a regular Python function:

```python
def test_loaded_file():
    assert loaded_file() == "  contents  "
```

We can run `pytest` for this specific test and see that everything passes as expected:

```bash
> pytest dagster_testing_tests/test_lesson_2.py::test_loaded_file
...
dagster_testing_tests/test_lesson_2.py .                                                          [100%]
```