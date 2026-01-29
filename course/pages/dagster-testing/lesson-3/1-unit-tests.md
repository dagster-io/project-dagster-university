---
title: 'Lesson 3: Unit tests'
module: 'dagster_testing'
lesson: '3'
---

# Unit tests

Unit tests are small, isolated tests that check individual pieces of code (usually functions or methods). They focus on testing one unit of functionality at a time, ensuring that each component behaves correctly in isolation.

Unit testing can help you:

* Catch bugs early to identify issues before they become bigger problems.
* Write reliable code to maintain functionality when making changes.
* Safely modify code knowing tests will catch regressions.
* Speed up development and deployment with Continuous Integration (CI).
* Improve documentation. Since unit tests are tied directly to the code itself, they can serve as a great form of documentation.

Unit tests in Python generally focus on a single function and ensure it works as expected:

```python
def my_func():
   return 5


def test_my_func():
   assert my_func() == 5
```

### Asset tests

Dagster assets are good candidates for unit tests. Since an asset is responsible for one aspect or node in the overall graph, by writing unit tests for a given asset, we can ensure that that isolated node is working as expected.

We will begin with the following asset:

```python
# src/dagster_testing/defs/assets/lesson_3.py
@dg.asset
def state_population_file() -> list[dict]:
    file_path = Path(__file__).absolute().parent / "../data/ny.csv"
    with open(file_path) as file:
        reader = csv.DictReader(file)
        return [row for row in reader]
```

The code above:

1. Determines the directory of the Python script being executed and appends `../data/ny.csv`.
2. Opens the `ny.csv` file.
3. Parses each row of the csv into dictionaries with `csv.DictReader`.
4. Returns the contents of that file as a `list[dict]`.

The `ny.csv` file contains the population for three cities in New York. So what would a unit test for this asset look like? Let's think about the test function above. Tests should be deterministic. Given the same input, we should always expect the same output. In this case our input will always be the same file. And based on the type annotations, we can always expect the same list of dictionaries:

```python
[
   {
      "City": "New York",
      "Population": "8804190",
   },
   {
      "City": "Buffalo",
      "Population": "278349",
   },
   {
      "City": "Yonkers",
      "Population": "211569",
   },
]
```

So what would a good test look like? Click **View answer** to view it.

```python {% obfuscated="true" %}
# tests/test_lesson_3.py
def test_state_population_file():
    assert lesson_3.state_population_file() == [
        {
            "City": "New York",
            "Population": "8804190",
        },
        {
            "City": "Buffalo",
            "Population": "278349",
        },
        {
            "City": "Yonkers",
            "Population": "211569",
        },
    ]
```

If you are familiar with Python testing, writing a test for an asset should look the same testing a standard Python function. We can use `pytest` library to execute this specific test to ensure everything works as intended.

To run this test, use the pytest CLI from the virtual environment:

```bash
> pytest tests/test_lesson_3.py::test_state_population_file
...
tests/test_lesson_3.py .                                                          [100%]
```