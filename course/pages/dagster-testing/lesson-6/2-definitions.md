---
title: 'Lesson 6: Definitions'
module: 'dagster_testing'
lesson: '6'
---

# Definitions

Within your Dagster project the most important object is the definition. This defines all the objects that will deployed into your code location. Because of its importance we will want to write a test for it.

Luckily this is a very easy test to write.

```python
from dagster_testing.definitions import defs

def test_def():
    assert defs
```

```bash
> pytest dagster_testing_tests/test_lesson_6.py::test_def
...
dagster_testing_tests/test_lesson_6.py .                                                          [100%]
```

As simple as it may seem, this test will find many issues associated with your Dagster project. This ensures that all the Dagster objects can load successfully and that certain dependencies between objects are satisfied (such a given resource being present if it is required for an asset). So if there is an issue loading any of your assets, asset checks, jobs, resources, schedules and sensors into the definition this test will trigger.

{% callout %}

> 💡 **Unit tests:** While this test will catch many issues, we still need individual tests to ensure that the assets and other Dagster objects __execute__ as expected. The definition test only ensures proper __loading__ of the objects.

> {% /callout %}

## Definition objects

As well as ensuring that the definition can load properly. You can include definition tests to ensure that the definition contains expected Dagster objects. Remember that only objects set within the definition will be deployed in the code location.

The `Definitions` object includes get methods for various object types. So we can check if certain objects are loaded.

```python
def test_def_objects():
    assert defs.get_assets_def("total_population")
    assert defs.get_job_def("jobs_config")
    assert defs.get_schedule_def("my_schedule")
    assert defs.get_sensor_def("my_sensor")
```

```bash
> pytest dagster_testing_tests/test_lesson_6.py::test_non_negative
...
dagster_testing_tests/test_lesson_6.py .                                                          [100%]
```

These tests can be helpful if you want to make sure that certain objects are present such as a critical asset or schedule.