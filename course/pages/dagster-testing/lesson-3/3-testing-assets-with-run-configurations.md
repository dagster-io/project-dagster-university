---
title: 'Lesson 3: Testing assets with run configurations'
module: 'dagster_testing'
lesson: '3'
---

# Testing assets with run configurations 

Some assets in Dagster pipelines may take in parameters defined outside of asset outputs. Typically, these are run configurations that are set at execution time. 

If we think about the `state_population_file` it can currently only parse a single file. Let's create a new asset called `state_population_file_config` with a run configuration. This asset will be able to process any file:

```python
# /dagster_testing/assets/unit_assets.py
class FilepathConfig(dg.Config):
    path: str


@dg.asset
def state_population_file_config(config: FilepathConfig) -> list[dict]:
    with open(config.path) as file:
        reader = csv.DictReader(file)
        return [row for row in reader]
```

Now let's write a new test for this asset. Since we can now provide any file. we will use the `test.csv` file in the `dagster_testing_tests/data` directory. This file has the same schema as our ny.csv file but includes some test data.

```
City,Population
Example 1,4500000
Example 2,3000000
Example 3,1000000
```

To test an asset with a run configuration, you will set the specific run configuration required by the asset as an input parameter. Here is what the test will look like. Click **View answer** to view it.

```python {% obfuscated="true" %}
def test_state_population_file_config():
    file_path = Path(__file__).absolute().parent / "data/test.csv"

    config = assets.FilepathConfig(path=file_path)
    assert unit_assets.state_population_file_config(config_file) == [
        {
            "City": "Example 1",
            "Population": "4500000",
        },
        {
            "City": "Example 2",
            "Population": "3000000",
        },
        {
            "City": "Example 3",
            "Population": "1000000",
        },
    ]
```

```bash
> pytest dagster_testing_tests/test_lesson_3.py::test_state_population_file_config
...
dagster_testing_tests/test_lesson_3.py .                                                          [100%]
```

## pytest fixtures

When testing with Dagster and `pytest` together, we can take advantage of some `pytest` functionality to make the testing code easier to reuse. If the `FilepathConfig` was used by multiple tests, we might benefit from creating a `pytest` fixture:

```python
@pytest.fixture()
def config_file():
    file_path = Path(__file__).absolute().parent / "data/test.csv"
    return unit_assets.FilepathConfig(path=file_path.as_posix())


def test_state_population_file_config_fixture_1(config_file):
    assert unit_assets.state_population_file_config(config_file) == [
        {
            "City": "Example 1",
            "Population": "4500000",
        },
        {
            "City": "Example 2",
            "Population": "3000000",
        },
        {
            "City": "Example 3",
            "Population": "1000000",
        },
    ]
```

```bash
> pytest dagster_testing_tests/test_lesson_3.py::test_state_population_file_config_fixture_1
...
dagster_testing_tests/test_lesson_3.py .                                                          [100%]
```

## Multiple pytext fixtures

Fixtures make testing code much easier to read and helps consolidate aspects that may be used by multiple tests. Tests can also use multiple fixtures. If we wanted to include an additional fixture for the output of the function.

```python
@pytest.fixture()
def config_file():
    file_path = Path(__file__).absolute().parent / "data/test.csv"
    return unit_assets.FilepathConfig(path=file_path.as_posix())


@pytest.fixture()
def file_example_output():
    return [
        {
            "City": "Example 1",
            "Population": "4500000",
        },
        {
            "City": "Example 2",
            "Population": "3000000",
        },
        {
            "City": "Example 3",
            "Population": "1000000",
        },
    ]


def test_state_population_file_config_fixture_2(config_file, file_example_output):
    assert unit_assets.state_population_file_config(config_file) == file_example_output
```

```bash
> pytest dagster_testing_tests/test_lesson_3.py::test_state_population_file_config_fixture_2
...
dagster_testing_tests/test_lesson_3.py .                                                          [100%]
```

## Passing run configuration to the materialization run

In order to provide the run configuration to the materialization run, we will need to specify an additional parameter called `run_config` within the call to `materialize()`. This parameter takes a `RunConfig` object that maps the specific run configuration to the asset that requires it:

```python
def test_assets_config(config_file, file_example_output):
    _assets = [
        unit_assets.state_population_file_config,
        unit_assets.total_population_config,
    ]
    result = dg.materialize(
        assets=_assets,
        run_config=dg.RunConfig({"state_population_file_config": config_file}),
    )
    assert result.success

    assert result.output_for_node("state_population_file_config") == file_example_output
    assert result.output_for_node("total_population_config") == 8500000
```

```bash
> pytest dagster_testing_tests/test_lesson_3.py::test_assets_config
...
dagster_testing_tests/test_lesson_3.py .                                                          [100%]
```

You can also pass in this configuration information with YAML in a format similar to the Dagster UI. Here is the same run configuration as YAML:

```yaml
ops:
  state_population_file_config:
    config:
      path: "dagster_testing_tests/data/test.csv"
```

Then we can update the `run_config` parameter to use that YAML file:

```python {% obfuscated="true" %}
def test_assets_config_yaml(file_example_output):
    _assets = [
        unit_assets.state_population_file_config,
        unit_assets.total_population_config,
    ]
    result = dg.materialize(
        assets=_assets,
        run_config=yaml.safe_load(
            (Path(__file__).absolute().parent / "configs/lesson_3.yaml").open()
        ),
    )
    assert result.success

    assert result.output_for_node("state_population_file_config") == file_example_output
    assert result.output_for_node("total_population_config") == 8500000
```

```bash
> pytest dagster_testing_tests/test_lesson_3.py::test_assets_config_yaml
...
dagster_testing_tests/test_lesson_3.py .                                                          [100%]
```

There is no difference between using `dg.RunConfig` or a YAML when running tests. You may find YAML easier to manage in more complex configurations for readability or to keep as examples for users who will run executions in the Dagster UI.