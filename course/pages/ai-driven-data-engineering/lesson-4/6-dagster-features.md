---
title: "Lesson 4: Dagster features — adding automation"
module: 'ai_driven_data_engineering'
lesson: '4'
---

# Dagster features: adding automation

Once the project and assets are in place, you can use the skill to add **automation**. For example, schedule the raw assets to run every day at 8:00 AM EST.

---

## Prompt

Ask the agent with the skill:

```bash
/dagster-expert Include scheduling for the assets for every day at 8am EST
```

The skill directs the agent to use Dagster’s scheduling abstractions (a job that selects the assets, plus a schedule) and to place them in the right files under `defs/`.

---

## What gets added

The agent will typically:

1. **Define or reuse a job** that selects the three raw assets (e.g. with `dg.define_asset_job` or an existing job in `defs/jobs.py`).
2. **Add a schedule** that runs that job daily at 8:00 AM EST.

For 8:00 AM EST, the cron expression is `0 8 * * *` when the scheduler’s time zone is set to America/New_York (or the equivalent in your deployment). The code might look like this:

```python
# defs/schedules.py (or similar)
import dagster as dg

from .jobs import raw_data_job  # or wherever the job is defined

raw_data_daily_schedule = dg.ScheduleDefinition(
    job=raw_data_job,
    cron_schedule="0 8 * * *",  # 8:00 AM daily
    execution_timezone="America/New_York",
)
```

The schedule is then included in the code location’s definitions (e.g. in `definitions.py` or via `defs/__init__.py`) so it shows up in the Dagster UI and runs on the defined cadence.

---

## Why this fits the skill

The skill knows where jobs and schedules live (e.g. `defs/jobs.py`, `defs/schedules.py`), how to wire them into `Definitions`, and how to use `dg scaffold` if new files are needed. So “add scheduling” becomes a single prompt that produces consistent, well-placed code instead of ad hoc edits. As you add more assets or schedules, reusing the same skill and `dg` workflow keeps the project tidy and predictable.
