---
title: 'Lesson 3: Mocks'
module: 'dagster_testing'
lesson: '3'
---

So far all of the assets we have created do not connect to other services. This is often not the case when building out a true data platform. Even a platform a small organization may connect to dozens of external systems.

We will create an asset to retrieve information from an API. [Open Library](https://openlibrary.org/dev/docs/api/search) is an online project intended to create "one web page for every book ever published". It maintains a public API that is free to use.

```python
API_URL = "https://openlibrary.org/search/authors.json"


@dg.asset
def author_works() -> list:
    output = []
    try:
        response = requests.get(API_URL, params={"q": "Twain"})
        response.raise_for_status()

        for doc in response.json().get("docs"):
            output.append(
                {
                    "author": doc.get("name"),
                    "top_work": doc.get("top_work"),
                }
            )

        return output

    except requests.exceptions.RequestException:
        return output
```

The code above:

1. Queries Open Library for all authors matching the name "Twain"
2. Parses the results and extract the "name" and "top work" for each author
3. Returns the data as a list

## Mocks

When writing tests for assets like this, we do not want to always connect to the external system being used. Either due to cost, time, security or any number of other factors, it is usually best to keep external dependencies separate from our unit tests which are intended to be a fast and predictable check on our code.

To help ensure the isolation of our Python code we can use mocks with `unittest.mock`. Mocks allow us to replace dependencies with controlled, predictable responses. To begin we can define an example response from the Open Library API:

```python
EXAMPLE_RESPONSE = {
    "numFound": 2,
    "docs": [
        {
            "name": "Mark Twain",
            "top_work": "Adventures of Huckleberry Finn",
        },
        {
            "name": "Mark Twain Media",
            "top_work": "Easy Science Experiments, Grades 4 - 6+",
        },
    ],
}
```

This is not all the data that is returned but includes the key fields we are interested in.

Next we will use [Mock](https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock) and configure the expected behavior:

```python
mock_response = Mock()
mock_response.json.return_value = EXAMPLE_RESPONSE
mock_response.raise_for_status.return_value = None
mock_get.return_value = mock_response
```

Using the code above we can override the `requests.get` method and ensure it returns the data from `EXAMPLE_RESPONSE`.

Now we can write a unit test and use the `@patch` decorator to set the method to our mocked behavior:

```python
@patch("requests.get")
def test_author(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = EXAMPLE_RESPONSE
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = author_works("twain")

    assert len(result) == 2
    assert result[0] == {
        "author": "Mark Twain",
        "top_work": "Adventures of Huckleberry Finn",
    }
    mock_get.assert_called_once_with(API_URL, params={"q": "Twain"})
```

We can still use pytest to run the test:

```bash
> pytest dagster_testing_tests/test_lesson_3.py::test_author
...
dagster_testing_tests/test_lesson_3.py .                                                          [100%]
```

The test completely bypasses the external API and returns our mocked data.