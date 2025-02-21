---
title: 'Lesson 3: Resources'
module: 'dagster_testing'
lesson: '3'
---

In Dagster you will not always see external dependencies defined directly within assets. Usually external dependencies are shared across multiple assets. This is where resources come in handy.

Dagster resources are objects that provide access to external systems, databases, or services, and are used to manage connections to these external systems within Dagster assets.

We can refactor the Open Library code we defined within our asset into a resource:

```python
class AuthorResource(dg.ConfigurableResource):
   def get_authors(self, author: str) -> list:
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

This resource contains a single method `get_authors` which returns the parsed author information from Open Library:

Next we can rewrite the asset to just use the resource:

```python
@dg.asset
def author_works_with_resource(author: str, author_resource: AuthorResource) -> list:
   return author_resource.get_authors(author)
```

## Testing resources

So how does this change the test? Click **View answer** to view it.

```python {% obfuscated="true" %}
@patch("requests.get")
def test_author_resource_mock(mock_get):
   mock_response = Mock()
   mock_response.json.return_value = EXAMPLE_RESPONSE
   mock_response.raise_for_status.return_value = None
   mock_get.return_value = mock_response

   result = author_works_with_resource(AuthorResource())

   assert len(result) == 2
   assert result[0] == {
       "author": "Mark Twain",
       "top_work": "Adventures of Huckleberry Finn",
   }
   mock_get.assert_called_once_with(API_URL, params={"q": "Twain"})
```

Surprisingly not much. We still will want to patch the `requests.get` method. Though now that method is invoked by the resource instead of the asset itself. From a testing perspective this does not make a difference so almost everything about our test remains.

The only difference is the `author_works_with_resource` asset requires an initialized `AuthorResource`.

## Materialize resource assets

When we discussed unit tests we showed how you can execute one or more assets together using `materialize`. We can still materialize even when using mocks.

```python
@patch("requests.get")
def test_author_assets(mock_get):
   mock_response = Mock()
   mock_response.json.return_value = EXAMPLE_RESPONSE
   mock_response.raise_for_status.return_value = None
   mock_get.return_value = mock_response


   result = dg.materialize(
       assets=[author_works_with_resource],
       resources={"author_resource": AuthorResource()},
   )
   assert result.success
```

We can also materialize with resources and configs together. Let's make a slight modification to our `author_works_with_resource` so it can take in a run configuration.

```python
class AuthorConfig(dg.Config):
   name: str


@dg.asset
def author_works_with_resource_config(
   config: AuthorConfig, author_resource: AuthorResource
) -> list:
   return author_resource.get_authors(config.name)
```

Now can execute a materialization that specifies both the `resource` and the `run_config`:

```python
@patch("requests.get")
def test_author_assets_config(mock_get):
   mock_response = Mock()
   mock_response.json.return_value = EXAMPLE_RESPONSE
   mock_response.raise_for_status.return_value = None
   mock_get.return_value = mock_response


   result = dg.materialize(
       assets=[author_works_with_resource_config],
       resources={"author_resource": AuthorResource()},
       run_config=dg.RunConfig(
           {"author_works_with_resource_config": AuthorConfig(name="Twain")}
       ),
   )
   assert result.success
```

Using `materialize` is very flexible and allows us to do almost anything we do via the Dagster UI when executing assets.

