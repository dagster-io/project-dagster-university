---
title: 'Lesson 3: Mocks'
module: 'dagster_testing'
lesson: '3'
---

Many of your assets will likely rely on services that extend outside of Dagster. Imagine an asset that pulls data from an API. This is a simple API that retrieves facts about authors from [Open Library](https://openlibrary.org/dev/docs/api/search).


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

1. Takes in an author name
2. Uses the Open Library API to return all authors matching the author name
3. Parse the result of the API and extract the "name" and "top work" for each author
4. Return the data as a list


## Mocks

When running unit tests we do not want to always connect to every service. Either due to cost, time, security or any number of other factors, it is usually best to keep using those services separate from our unit tests.

To accomplish this in Python we can use mocks with `unittest.mock`. Mocks allow you to replace dependencies with controlled, predicatble responses. To begin we can define an example reponse from 

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


```python
mock_response = Mock()
mock_response.json.return_value = EXAMPLE_RESPONSE
mock_response.raise_for_status.return_value = None
mock_get.return_value = mock_response
```



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