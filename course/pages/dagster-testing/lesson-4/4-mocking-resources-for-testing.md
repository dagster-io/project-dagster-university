---
title: 'Lesson 4: Mocking resources for testing'
module: 'dagster_testing'
lesson: '4'
---

# Mocking resources for testing

When using mocks and resources together, it can sometimes be easier to mock the resource itself rather than the underlying function. We can avoid patching `requests.get` altogether and instead mock the `StatePopulation` resource.

Think back to the two questions to consider when mocking a service:

1. What service you are trying to emulate.
2. How the emulated service should function in order to satisfy the test.

Now we want to emulate `StatePopulation`. In terms of what functionality we need, we need to mock the response of the `get_cities` method. This means we do not have to worry about `requests`. 

First we will create another `pytest.fixture` for an example response from `get_cities`.

```python
@pytest.fixture
def fake_city():
    return {
        "city": "Fakestown",
        "population": 42,
    }
```

Next we will set a mock for the return value.

```python
mocked_resource = Mock()
mocked_resource.get_cities.return_value = [fake_city]
```

This is everything we need to write a new test for the `state_population_api_resource` asset. Remember there is no need for the patch decorator anymore because `requests` is not needed. What would the test look like? Click **View answer** to view it.

```python {% obfuscated="true" %}
def test_state_population_api_mocked_resource(fake_city):
    mocked_resource = Mock()
    mocked_resource.get_cities.return_value = [fake_city]

    result = lesson_4.state_population_api_resource(mocked_resource)

    assert len(result) == 1
    assert result[0] == fake_city
```

# Mocked resources with materialization

The mocked resource can also be used with `dg.materialize()` if we wanted to run multiple assets in a single test:

```python 
def test_state_population_api_assets_mocked_resource(fake_city):
    mocked_resource = Mock()
    mocked_resource.get_cities.return_value = [fake_city]

    result = dg.materialize(
        assets=[
            lesson_4.state_population_api_resource_config,
            lesson_4.total_population_resource_config,
        ],
        resources={"state_population_resource": mocked_resource},
        run_config=dg.RunConfig(
            {"state_population_api_resource_config": lesson_4.StateConfig(name="ny")}
        ),
    )
    assert result.success

    assert result.output_for_node("state_population_api_resource_config") == [fake_city]
    assert result.output_for_node("total_population_resource_config") == 42
```

```bash
> pytest dagster_testing_tests/test_lesson_4.py::test_state_population_api_assets_mocked_resource
...
dagster_testing_tests/test_lesson_4.py .                                                          [100%]
```

## When to mock a resource

You might be wondering when you should mock a resource as opposed to mocking the functions used within the resource. Generally you should mock the methods used by the resource if you are more concerned about testing the functionality of the resource and can mock the methods of the resource if you are more concerned with testing the functionality of the assets.

Mocking the resource itself can also help give you more control over the specific output expected for certain functions. This will make it easier when writing tests for assets that use multiple resources or resources that maintain state.
