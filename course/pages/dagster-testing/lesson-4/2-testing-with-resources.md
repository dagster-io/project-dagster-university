---
title: 'Lesson 4: Testing with resources'
module: 'dagster_testing'
lesson: '3'
---

# Testing with resources

In Dagster you will not always see external dependencies defined directly within assets. Usually external dependencies are shared across multiple assets. This is where resources come in handy.

Dagster resources are objects that provide access to external systems, databases, or services, and are used to manage connections to these external systems within Dagster assets.

We can refactor the API asset code into a resource:

```python
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

This resource contains a single method `get_cities` which would return the parsed results from the API endpoint.

Next we can rewrite the asset to just use the resource:

```python
@dg.asset
def state_population_api_resource(
    state_population_resource: StatePopulation,
) -> list[dict]:
    return state_population_resource.get_cities("ny")
```

## Testing resources

So how does this change the test? Click **View answer** to view it.

```python {% obfuscated="true" %}
@patch("requests.get")
def test_state_population_api_resource_mock(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = EXAMPLE_RESPONSE
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = assets.state_population_api_resource(assets.StatePopulation())

    assert len(result) == 2
    assert result[0] == {
        "city": "New York",
        "population": 8804190,
    }
    mock_get.assert_called_once_with(assets.API_URL, params={"state": "ny"})
```

Surprisingly not much. We still will want to patch the `requests.get` method. Though now that method is invoked by the resource instead of the asset itself. From a testing perspective this does not make a difference so almost everything about our test remains.

The only difference is the `state_population_api_resource` asset requires an initialized `StatePopulation` resource.

## Materialize resource assets

When we discussed unit tests we showed how you can execute one or more assets together using `materialize`. We can still materialize our assets even when using mocks.

```python
@patch("requests.get")
def test_state_population_api_assets(mock_get, api_output):
    mock_response = Mock()
    mock_response.json.return_value = EXAMPLE_RESPONSE
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = dg.materialize(
        assets=[
            assets.state_population_api_resource,
            assets.total_population_resource,
        ],
        resources={"state_population_resource": assets.StatePopulation()},
    )
    assert result.success

    assert result.output_for_node("state_population_api_resource") == api_output
    assert result.output_for_node("total_population_resource") == 9082539
```

We can also materialize with resources and configs together. Let's make a slight modification to our `author_works_with_resource` so it can take in a run configuration.

```python
class StateConfig(dg.Config):
    name: str


@dg.asset
def state_population_api_resource_config(
    config: StateConfig, state_population_resource: StatePopulation
) -> list:
    return state_population_resource.get_cities(config.name)
```

Now can execute a materialization that specifies both the `resource` and the `run_config`:

```python
@patch("requests.get")
def test_state_population_api_assets_config(mock_get, api_output):
    mock_response = Mock()
    mock_response.json.return_value = EXAMPLE_RESPONSE
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = dg.materialize(
        assets=[
            assets.state_population_api_resource_config,
            assets.total_population_resource_config,
        ],
        resources={"state_population_resource": assets.StatePopulation()},
        run_config=dg.RunConfig(
            {"state_population_api_resource_config": assets.StateConfig(name="ny")}
        ),
    )
    assert result.success
```

Using `materialize` is very flexible and allows us to do almost anything we do via the Dagster UI when executing assets.

