---
title: 'Lesson 7: Practice: Create a weekly_update_job'
module: 'dagster_essentials'
lesson: '7'
---

# Practice: Create a weekly_update_job

To practice what you’ve learned, add a job to `src/dagster_essentials/defs/jobs.py` that will materialize the `trips_by_week` asset.

---

## Check your work

The job you built should look similar to the following code. Click **View answer** to view it.

**If there are differences**, compare what you wrote to the job below and change them, as this job will be used as-is in future lessons.

```python {% obfuscated="true" %}
import dagster as dg

trips_by_week = dg.AssetSelection.assets(["trips_by_week"])

weekly_update_job = dg.define_asset_job(
    name="weekly_update_job",
    selection=trips_by_week,
)
```
