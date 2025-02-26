---
title: 'Lesson 4: Mocking resources for testing'
module: 'dagster_testing'
lesson: '3'
---

# Mocking resources for testing

When using mocks and resources together, it can sometimes be easier to mock the methods of the resource itself.

The `get_cities` method within the `StatePopulation` resource returns the data from the API after it has been processed. So if we wanted to setup a mock for the response from the resource, it would be slightly different: 

```python
fake_city = {
   "city": "Fakestown",
   "population": 42,
}

mocked_resource = Mock()
mocked_resource.get_cities.return_value = [fake_city]
```

You can see that we are no longer setting up the mock around `get` and instead are mocking and setting the return value for `get_cities` method in the resource.

Now when we run the `state_population_api_resource` we can supply our mocked version of the resource rather than an actual initialized `StatePopulation` resource. Click **View answer** to view it.

```python {% obfuscated="true" %}
def test_state_population_api_mocked_resource():
    fake_city = {
        "city": "Fakestown",
        "population": 42,
    }

    mocked_resource = Mock()
    mocked_resource.get_cities.return_value = [fake_city]

    result = assets.state_population_api_resource(mocked_resource)

    assert len(result) == 1
    assert result[0] == fake_city
```

There is no longer a need to patch `requests.get` because the mocked version of the resource completely bypasses the any need for an API.

## When to mock a resource

You might be wondering when you should mock a resource as opposed to mocking the methods used. Generally speaking you should mock the methods used by the resource if you are more concerned about testing the functionality of the resource and can mock the methods of the resource if you are more concerned with testing the functionality of the assets.

Mocking a resource itself can help give you more control over the specific output expected for certain functions. This can help make it easier when writing tests for assets that use multiple resources.

