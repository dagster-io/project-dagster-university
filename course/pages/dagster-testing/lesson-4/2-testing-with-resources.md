---
title: 'Lesson 4: Testing with resources'
module: 'dagster_testing'
lesson: '4'
---

# Testing with resources

In Dagster you will not always see external dependencies defined directly within assets. Usually external dependencies are reused and shared across multiple assets. This is where resources come in handy.

Resources are objects that provide access to external systems, databases, or services, and are used to manage dependencies within Dagster.

We can refactor the API asset code into a resource. A resource is just a class that inherits from `dg.ConfigurableResource`. It can have any number of methods which assets can use. This resource will only include a single method for `get_cities`.

```python
# /dagster_testing/defs/assets/lesson_4.py
class StatePopulation(dg.ConfigurableResource):
    def get_cities(self, state: str) -> list[dict]:
        output = []
        try:
            response = requests.get(API_URL, params={"state": state})
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

This code is almost unchanged from the `state_population_api` asset. It connects to the API, retrieves the JSON, and returns the parsed results.

Since the resource now contains all the logic for connecting to the API, we can write a new asset that invokes the method:

```python
@dg.asset
def state_population_api_resource(
    state_population_resource: StatePopulation,
) -> list[dict]:
    return state_population_resource.get_cities("ny")
```

## Testing resources

Our asset is different. Now in order to execute it will require an initialized `StatePopulation` resource:

```python
assets.state_population_api_resource(assets.StatePopulation())
```

But we left the core logic unchanged. So what needs to change in our test? Click **View answer** to view it.

```python {% obfuscated="true" %}
@patch("requests.get")
def test_state_population_api_resource_mock(mock_get, example_response):
    mock_response = Mock()
    mock_response.json.return_value = example_response
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = lesson_4.state_population_api_resource(lesson_4.StatePopulation())

    assert len(result) == 2
    assert result[0] == {
        "city": "New York",
        "population": 8804190,
    }
    mock_get.assert_called_once_with(lesson_4.API_URL, params={"state": "ny"})

```

```bash
> pytest tests/test_lesson_4.py::test_state_population_api_resource_mock
...
tests/test_lesson_4.py .                                                          [100%]
```

Surprisingly not much. We still will want to patch the `requests.get` method so all of our set up with mocks remains the same. The main difference is that the `request` method is invoked by the resource instead of the asset itself. From a testing perspective this does not make a difference so almost everything about our test remains.
