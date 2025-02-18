---
title: 'Lesson 2: Configs'
module: 'dagster_testing'
lesson: '2'
---

Some assets in our pipelines might be dynamic and set at execution time with a run configuration. Let's rework the `loaded_file` asset to take in a configuration so it can accept any file.

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

Now let's write a new test to ensure that the file in the tests directory `path.txt` works as expected. **Hint** The contents of that file is "  example  ".

```python {% obfuscated="true" %}
def test_loaded_file_config():
    config = FilepathConfig(path="path.txt")
    loaded_file_config(config) == "  example  "
```

## Pytest fixtures

Testing with Dagster does not prevent us from using other traditional pytest practices. If that `FilepathConfig` was used by multiple tests. We might benefit from creating a pytest fixture that can be easily reused:

```python
@pytest.fixture()
def example_config():
    return FilepathConfig(path="path.txt")


def test_loaded_file_config_fixture(example_config):
    loaded_file_config(example_config) == "  example  "
```

## Config pipelines

The final thing to mention about configs is how to pass them in if we want to structure a test around `materialize`. In order to provide the run configuration to materialize, we will need an additional parameter:

```python
def test_assets_config():
    assets = [
        loaded_file_config,
        processed_file_config,
    ]
    result = dg.materialize(
        assets=assets,
        run_config=yaml.safe_load(
            (Path(__file__).absolute().parent / "lesson_1_run_config.yaml").open()
        ),
    )
    assert result.success
```

Here we are providing the `run_config` by parsing the contents of a yaml file:

```yaml
ops:
  loaded_file_config:
    config:
      path: "path.txt"
```

This yaml format matches the yaml sync that is required in the Dagster UI when you launch a pipeline that has a run configuration.

How would you add to the `test_assets_config` test to ensure the output of the assets matches what is expected?

```python {% obfuscated="true" %}
def test_assets_config():
    assets = [
        loaded_file_config,
        processed_file_config,
    ]
    result = dg.materialize(
        assets=assets,
        run_config=yaml.safe_load(
            (Path(__file__).absolute().parent / "lesson_1_run_config.yaml").open()
        ),
    )
    assert result.success

    # Ensure assets return expected results
    result.output_for_node("loaded_file_config") == "  example  "
    result.output_for_node("processed_file_config") == "example"
```