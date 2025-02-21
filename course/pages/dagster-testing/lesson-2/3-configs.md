---
title: 'Lesson 2: Configs'
module: 'dagster_testing'
lesson: '2'
---

Some assets in our pipelines may take in parameters defined outside of asset outputs. Typically these are run configurations that are set at execution time. Let's rework the `loaded_file` asset to take in a run configuration so it processes different files.

```python
class FilepathConfig(dg.Config):
   path: str


@dg.asset
def loaded_file_config(config: FilepathConfig) -> str:
   current_file_path = os.path.dirname(os.path.realpath(__file__))
   file_name = os.path.join(current_file_path, config.path)
   with open(file_name) as file:
       return file.read()
```

Now let's write a new test to ensure that the file in the tests directory `path.txt` works as expected (the contents of that file is "  example  ").

```python {% obfuscated="true" %}
def test_loaded_file_config():
    config = FilepathConfig(path="path.txt")
    loaded_file_config(config) == "  example  "
```

## Pytest fixtures

Testing with Dagster and pytest together we take advantage of some pytest functionality to make the testing code easier to reuse. If the `FilepathConfig` was used by multiple tests, we might benefit from creating a pytest fixture:

```python
@pytest.fixture()
def example_config():
    return FilepathConfig(path="path.txt")


def test_loaded_file_config_fixture(example_config):
    loaded_file_config(example_config) == "  example  "
```

## Config pipelines

The final thing to mention about configs is how to pass them to the materialization run. In order to provide the run configuration, we will need an additional parameter `run_config` within `materialize`. This will take in a `RunConfig` that maps the specific run configuration to the asset that requires it:

```python
def test_assets_config():
    assets = [
        loaded_file_config,
        processed_file_config,
    ]
    result = dg.materialize(
        assets=assets,
        run_config=dg.RunConfig(
            {
                "loaded_file_config": FilepathConfig(path="path.txt")
            }
        ),
    )
    assert result.success

    result.output_for_node("loaded_file_config") == "  example  "
    result.output_for_node("processed_file_config") == "example"
```

You can also pass in this information via yaml in a format similar to the Dagster UI. Here is the same run configuration as yaml:

```yaml
ops:
  loaded_file_config:
    config:
      path: "path.txt"
```

Then we can update the `run_config` to use that yaml file:

```python {% obfuscated="true" %}
def test_assets_config_yaml():
    assets = [
        loaded_file_config,
        processed_file_config,
    ]
    result = dg.materialize(
        assets=assets,
        run_config=yaml.safe_load(
            (Path(__file__).absolute().parent / "configs/lesson_2.yaml").open()
        ),
    )
    assert result.success

    result.output_for_node("loaded_file_config") == "  example  "
    result.output_for_node("processed_file_config") == "example"
```