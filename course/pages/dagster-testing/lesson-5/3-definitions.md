---
title: 'Lesson 5: Definitions'
module: 'dagster_testing'
lesson: '5'
---

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
        "number": resources.ExampleResource(api_key="ABC123"),
    },
    schedules=[schedules.my_schedule],
    sensors=[sensors.my_sensor],
)
```

We will still want individual tests to ensure that the assets defined in the definitions are behaving as intended. But this one test can catch a good deal of issues.
