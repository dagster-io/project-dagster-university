---
title: 'Lesson 4: Testing with mocks'
module: 'dagster_testing'
lesson: '4'
---

# Testing with mocks

So far none of the assets we created connect to other services. This is often not the case when building out a true data platform. Even the platform for a small organization will use dozens of external systems.

In lesson 2 our pipeline brought in city population data from a CSV stored locally. What would it look like instead we queried an API to get city data?

Imagine that an API exists to query city populations by state (sadly this API does not exist in real life but it will not matter for our testing purposes). Let's say the API endpoint exists at `fake.com` and a sample request for a specific state would look like.

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

We want to rewrite the `state_population_file` asset to use this endpoint instead of reading a file to retrieve the necessary data. This is what the new asset will look like.

```python
# /dagster_testing/defs/assets/lesson_4.py
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

1. Queries the imaginary API for the state "ny".
2. Extracts the JSON from the API response.
3. Parses the JSON and extract the "name" and "population" for each city.
4. Returns the data as a list of dictionaries.

This all makes sense but how will we test this asset? Especially considering this API does not even exist.

## Mocks

When writing tests we do not want to always connect to the external system being used. Either due to cost, time, security or any number of other factors, it is usually best to keep external dependencies separate from our unit tests which are intended to be fast and predictable checks on our code.

{% callout %}
> 💡 You can use tests that connect to live systems and we will discuss them in the next lesson.
{% /callout %}

To help ensure the isolation of our Python code we can use mocks with `unittest.mock`. Mocks allow us to replace dependencies with controlled responses. When using mocks you should think about:

1. What service you are trying to emulate.
2. How the emulated service should function in order to satisfy the test.

We can start by thinking about the service we need to replace. In this case it is the API `fake.com`. We access the API through the Python `requests` library. So we will need to emulate that in our test.

Next we can think about what is returned by that API call. We know the structure of the JSON so we can create a `pytest.fixture` with a sample of what the data may look like.

```python
@pytest.fixture
def example_response():
    return {
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

Now we need to set the `get` function in `requests` to return our example response.  We will use [Mock](https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock) to set this behavior behavior:

```python
mock_response = Mock()
mock_response.json.return_value = example_response
mock_response.raise_for_status.return_value = None
```

This creates a mock and sets the return value for `json()` to our example response. We can now move this piece of code into a test. We will decorate the test function with `@patch` which will temporarily replace the object being patched. In this case `requests.get` will be patched.

```python
@patch("requests.get")
def test_state_population_api(mock_get, example_response):
    mock_response = Mock()
    mock_response.json.return_value = example_response
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = lesson_4.state_population_api()

    assert len(result) == 2
    assert result[0] == {
        "city": "New York",
        "population": 8804190,
    }
    mock_get.assert_called_once_with(lesson_4.API_URL, params={"state": "ny"})
```

The code above:

1. Temporarily replaced `requests.get`.
2. Uses the patched object as in input parameter along with the fixture `example_response`.
3. Creates a `Mock()` and sets the return value for `json()` to `example_response`.
4. Sets the return value for the patched object `mock_get` to the mocked response.
5. Executes the asset.
6. Uses `assert` to ensure the output of the asset matches what we expect from the mock.
7. Ensures that the mock was successfully called with the correct URL and parameters.

We can still use pytest to run the test.

```bash
> pytest dagster_testing_tests/test_lesson_4.py::test_state_population_api
...
dagster_testing_tests/test_lesson_4.py .                                                          [100%]
```

The test completely bypasses the API and returns our mocked data.
