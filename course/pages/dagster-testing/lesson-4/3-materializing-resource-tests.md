---
title: 'Lesson 4: Materializing resource tests'
module: 'dagster_testing'
lesson: '4'
---

# Materializing resource tests

When we discussed unit tests we showed how you can execute one or more assets together using `dg.materialize()`. We can still materialize our assets this way using mocks.

```python
# /tests/test_lesson_4.py
@patch("requests.get")
def test_state_population_api_assets(mock_get, example_response, api_output):
    mock_response = Mock()
    mock_response.json.return_value = example_response
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = dg.materialize(
        assets=[
            lesson_4.state_population_api_resource,
            lesson_4.total_population_resource,
        ],
        resources={"state_population_resource": lesson_4.StatePopulation()},
    )
    assert result.success

    assert result.output_for_node("state_population_api_resource") == api_output
    assert result.output_for_node("total_population_resource") == 9082539

```

```bash
> pytest tests/test_lesson_4.py::test_state_population_api_assets
...
tests/test_lesson_4.py .                                                          [100%]
```

This uses the same patch and mocked object as before. The only difference is that because there is an asset that requires a resource, it must be initialized and set within `dg.materialize()`.

## Testing with materialize and config

We can also materialize resources and configs together. We will make a slight modification to our `state_population_api_resource_config` so it can take in a run configuration.

```python
# src/dagster_testing/defs/assets/lesson_4.py
class StateConfig(dg.Config):
    name: str


@dg.asset
def state_population_api_resource_config(
    config: StateConfig, state_population_resource: StatePopulation
) -> list:
    return state_population_resource.get_cities(config.name)
```

Now it can be executed with the name of any state.

If we wanted to make a test using this new asset, we will need to specify both the `resource` and the `run_config` in `dg.materialize()`.

```python
# tests/test_lesson_4.py
@patch("requests.get")
def test_state_population_api_assets_config(mock_get, example_response, api_output):
    mock_response = Mock()
    mock_response.json.return_value = example_response
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = dg.materialize(
        assets=[
            lesson_4.state_population_api_resource_config,
            lesson_4.total_population_resource_config,
        ],
        resources={"state_population_resource": lesson_4.StatePopulation()},
        run_config=dg.RunConfig(
            {"state_population_api_resource_config": lesson_4.StateConfig(name="ny")}
        ),
    )
    assert result.success

    assert result.output_for_node("state_population_api_resource_config") == api_output
    assert result.output_for_node("total_population_resource_config") == 9082539
```

```bash
> pytest tests/test_lesson_4.py::test_state_population_api_assets_config
...
tests/test_lesson_4.py .                                                          [100%]
```

`dg.materialize()` is very flexible for testing and allows us to do almost anything that is possible in the Dagster UI when executing assets.