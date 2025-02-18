---
title: 'Lesson 3: Resources'
module: 'dagster_testing'
lesson: '3'
---

In Dagster you will not always see external dependencies defined directly within the assets themselves. It may be useful to define that external dependency separately and share it across multiple assets. This is where resources come in handy.

We can rewrite the code from the previous asset into a resource. This resource will have a single method `get_authors` which returns the parsed author information from Open Library:

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

Now we can rewrite the asset to just use the resource:

```python
@dg.asset
def author_works_with_resource(author: str, author_resource: AuthorResource) -> list:
    return author_resource.get_authors(author)
```

So how does this change the test? Surprisingly not much. We still will want to patch the `requests.get` method that is invoked by the resource. So almost everything about our test remains the same except for having to execute the asset with the resource:

```python
@patch("requests.get")
def test_author_resource_mock(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = EXAMPLE_RESPONSE
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = author_works_with_resource("twain", AuthorResource())

    assert len(result) == 2
    assert result[0] == {
        "author": "Mark Twain",
        "top_work": "Adventures of Huckleberry Finn",
    }
    mock_get.assert_called_once_with(API_URL, params={"q": "twain"})
```

## Materialize resource assets

When we discussed unit tests we showed how you can execute one or more assets together using `materialize`. We can still use materialize even when mocking.

First in order to provide the parameter (author) necessary to execute our asset. Let's make a slight modification to our `author_works_with_resource` so it can take in a run configuration.

```python
class AuthorConfig(dg.Config):
    name: str


@dg.asset
def author_works_with_resource_config(
    config: AuthorConfig, author_resource: AuthorResource
) -> list:
    return author_resource.get_authors(config.name)
```

Next we will define the yaml to use in the test.

```yaml
ops:
  author_works_with_resource_config:
    config:
      name: "Twain"
```

Finally we will define the test itself. We will reuse all the mocking from above and patch `requests.get`. Then we will use `dg.materialize` to execute the asset:

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
        run_config=yaml.safe_load(
            (Path(__file__).absolute().parent / "lesson_3_run_config.yaml").open()
        ),
    )
    assert result.success
```

Just as it would be necessary to supply the resource and the configuration if we were to run this asset in the UI, they will be set in `resources` and `run_config` respectively in `dg.materialize`.