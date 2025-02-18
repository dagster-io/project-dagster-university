---
title: 'Lesson 3: Mocks'
module: 'dagster_testing'
lesson: '3'
---

Many of your assets will likely rely on services that extend outside of Dagster. Imagine an asset that pulls data from an API. This is a simple API ([Open Library](https://openlibrary.org/dev/docs/api/search)) retrieves facts about authors.

It is easy enough to write an asset that returns data from the API and does some minimal parsing:

```python
import requests

API_URL = "https://openlibrary.org/search/authors.json"


@dg.asset
def author_works(author: str) -> list:
    output = []
    try:
        response = requests.get(API_URL, params={"q": author})
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

1. Takes in an author name as an asset parameter
2. Uses Open Library API to query all authors matching the author name
3. Parses the results and extract the "name" and "top work" for each author
4. Returns the data as a list

## Mocks

When writing tests for assets like this, we do not want to always connect to the external services being used. Either due to cost, time, security or any number of other factors, it is usually best to keep external dependencies separate from our unit tests.

To accomplish this level of isolation in Python we can use mocks with `unittest.mock`. Mocks allow you to replace dependencies with controlled, predictable responses. To begin we can define an example response from the API. This is not all the data that is returned but includes the key fields we are interested in:

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

Next we will use [Mock](https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock) and configure it to match the behavior we would expect from the actual service. However we are specifically setting the return value to be the `EXAMPLE_RESPONSE` we set above: 

```python
mock_response = Mock()
mock_response.json.return_value = EXAMPLE_RESPONSE
mock_response.raise_for_status.return_value = None
mock_get.return_value = mock_response
```

Using the code above we can override the `requests.get` method when testing our asset. Now we can write a unit test and use the `@patch` decorator to set the method to our mock behavior:

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
    mock_get.assert_called_once_with(API_URL, params={"q": "twain"})
```

Now when the test runs, we can ensure it is working as expected.