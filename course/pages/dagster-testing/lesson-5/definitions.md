---
title: 'Lesson 5: Definitions'
module: 'dagster_testing'
lesson: '5'
---

One test that you will see throughout the Dagster codebase and easiest to configure is a test to ensure you definitions can be loaded successfully. This test is as simple as:

```python
def test_def():
    assert defs
```

This will ensure that all objects loaded into your definitions are correctly configured and can be loaded. This two line test ensures that everything for the definition for this lesson:

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

Is correctly set. We will still want individual tests to ensure that the assets defined in the definitions are behaving as intended. But this one test goes can catch a good deal of issues.

Issues this can catch:
- 