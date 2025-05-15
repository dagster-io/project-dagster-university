---
title: 'Lesson 7: Creating a schedule'
module: 'dagster_essentials'
lesson: '7'
---

# Creating a schedule

Now that you know what makes up a schedule, let’s create one. To do this, we’ll use the `ScheduleDefinition` class.

We can use `dg` again to scaffold our schedules. So first run:

```bash
dg scaffold dagster.schedule schedules.py
```

This will create a file in `defs/schedules.py` where we can add the following schedule code:

```python
import dagster as dg
from dagster_essentials.defs.jobs import trip_update_job

trip_update_schedule = dg.ScheduleDefinition(
    job=trip_update_job,
    cron_schedule="0 0 5 * *", # every 5th of the month at midnight
)
```

Let’s look at what this code does:

1. Imports the `ScheduleDefinition` class
2. From the `jobs` module, import the `trip_update_job` job
3. Used `ScheduleDefinition` to create a schedule that:
   - Is attached to the `trip_update_job` job
   - Has a cron expression of `0 0 5 * *`

## Checking our schedule

To ensure the schedule is working as expected we can run a quick `dg check defs` to make sure everything loads correctly. Next we can rerun `dg list` to see that schedules are now included as part of the output.

```bash
> dg list defs
...
Schedules
┏━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ Name                     ┃ Cron schedule ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ trip_update_job_schedule │ 0 0 5 * *     │
└──────────────────────────┴───────────────┘
```