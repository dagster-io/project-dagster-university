---
title: 'Lesson 4: Testing with mocks'
module: 'dagster_testing'
lesson: '3'
---

# Testing with mocks

So far none of the assets we created connect to other services. This is often not the case when building out a true data platform. Even a platform a small organization may connect to dozens of external systems.

In lesson 2 our pipeline brought in city population data from a CSV stored locally. What would it look like instead we queried an API to get city data.

Imagine that an API exists to query city populations by state (sadly this API does not exist in real life but it will not matter for testing). Let's say the API endpoint exists at `fake.com` and a sample request would like:

```bash
> curl -X GET "https://fake.com/population.json?state=ny" -H "Accept: application/json"

{
  "cities": [
    {"name": "New York City", "population": 8804190},
    {"name": "Buffalo", "population": 278349},
    {"name": "Rochester", "population": 211328},
    {"name": "Yonkers", "population": 201344},
    {"name": "Syracuse", "population": 148620}
    ...
  ]
}
```

Now we can rework the `state_population_file` to instead use this API to pull our city population data: 

```python
API_URL = "https://fake.com/population.json"


@dg.asset
def state_population_api() -> list[dict]:
    output = []
    try:
        response = requests.get(API_URL, params={"state": "ny"})
        response.raise_for_status()

        for doc in response.json().get("cities"):
            output.append(
                {
                    "city": doc.get("city_name"),
                    "population": doc.get("city_population"),
                }
            )

        return output

    except requests.exceptions.RequestException:
        return output
```

The code above:

1. Queries the imaginary API for the state "ny"
2. Parses the results and extract the "name" and "population" for each city
3. Returns the data as a list of dictionaries

## Mocks

When writing tests for assets like this, we do not want to always connect to the external system being used. Either due to cost, time, security or any number of other factors, it is usually best to keep external dependencies separate from our unit tests which are intended to be a fast and predictable check on our code.

To help ensure the isolation of our Python code we can use mocks with `unittest.mock`. Mocks allow us to replace dependencies with controlled, predictable responses. To begin we can define an example response from the Open Library API:

```python
EXAMPLE_RESPONSE = {
    "cities": [
        {
            "city_name": "New York",
            "city_population": 8804190,
        },
        {
            "city_name": "Buffalo",
            "city_population": 278349,
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
def test_state_population_api(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = EXAMPLE_RESPONSE
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = assets.state_population_api()

    assert len(result) == 2
    assert result[0] == {
        "city": "New York",
        "population": 8804190,
    }
    mock_get.assert_called_once_with(assets.API_URL, params={"state": "ny"})
```

We can still use pytest to run the test:

```bash
> pytest dagster_testing_tests/test_lesson_3.py::test_state_population_api
...
dagster_testing_tests/test_lesson_3.py .                                                          [100%]
```

The test completely bypasses the external API and returns our mocked data.