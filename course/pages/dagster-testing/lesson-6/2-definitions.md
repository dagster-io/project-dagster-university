---
title: 'Lesson 6: Definitions'
module: 'dagster_testing'
lesson: '5'
---

# Definitions

We discussed some of the tests for the different objects in Dagster. But there is one object that all Dagster projects should have a test for. You will want to make sure that each code location can properly load the definitions:

```python
from dagster_testing.lesson_5.definitions import defs

def test_def():
    assert defs
```

This test will find most issues with any of the Dagster objects in our project. Which in this case covers assets, asset checks, jobs, resources, schedules and sensors:

```python
defs = dg.Definitions(
    assets=all_assets,
    asset_checks=[assets.non_negative],
    jobs=[jobs.my_job, jobs.my_job_configured],
    resources={
        "state_population_resource": resources.StatePopulation(),
    },
    schedules=[schedules.my_schedule],
    sensors=[sensors.my_sensor],
)
```

We will still want individual tests to ensure that the assets defined in the definitions are behaving as intended. But this one test can catch a good deal of issues.

## Definition objects

As well as ensuring that the definition can load properly. You can also ensure that it contains the expected objects. Remember that only objects set within the definition will be deployed.

The `Definitions` object has get methods to ensure that various object types are present within the definitions. So we can check if certain objects are loaded:

```python
def test_def_objects():
    assert defs.get_assets_def("total_population")
    assert defs.get_job_def("jobs_config")
    assert defs.get_schedule_def("my_schedule")
    assert defs.get_sensor_def("my_sensor")
```