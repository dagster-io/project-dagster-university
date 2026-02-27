---
title: "Lesson 4: Dagster features — adding automation"
module: 'ai_driven_data_engineering'
lesson: '4'
---

# Dagster features: adding automation

Once the project and assets are in place, you can use the skill to add automation. For example, schedule the raw assets to run every day at 8:00 AM EST.

## Prompt

Ask the agent to include a automation for the assets created so they execute every day at 8am EST:

```bash {% obfuscated="true" %}
> /dagster-expert Add a daily schedule that runs the raw assets every day at 8am EST.
```

The skill directs the agent to use Dagster’s scheduling abstractions (a job that selects the assets, plus a schedule) and to place them in the right files under `defs/`.

## What gets added

The agent will:

1. Define or reuse a job that selects the three raw assets (e.g. with `dg.define_asset_job` or an existing job in `defs/jobs.py`).
```python {% obfuscated="true" %}
# /src/university/defs/schedules/daily_raw.py
raw_ingestion_job = dg.define_asset_job(
    name="raw_ingestion_job",
    selection=dg.AssetSelection.groups("raw")
    - dg.AssetSelection.assets(trending_events),
)
```
2. Add a schedule that runs that job daily at 8:00 AM EST.
```python {% obfuscated="true" %}
# /src/university/defs/schedules/daily_raw.py
daily_raw_schedule = dg.ScheduleDefinition(
    name="daily_raw_8am_est",
    job=raw_ingestion_job,
    cron_schedule="0 8 * * *",
    execution_timezone="America/New_York",
    description="Materialize all raw assets every day at 8 AM Eastern.",
    default_status=dg.DefaultScheduleStatus.RUNNING,
)
```

The skill knows where jobs and schedules live (e.g. `defs/jobs.py`, `defs/schedules.py`), how to wire them into `Definitions`, and how to use `dg scaffold` if new files are needed. So “add scheduling” becomes a single prompt that produces consistent, well-placed code instead of ad hoc edits. As you add more assets or schedules, reusing the same skill and `dg` workflow keeps the project tidy and predictable.

The schedule is then included in the code location’s definitions (e.g. in `definitions.py` or via `defs/__init__.py`) so it shows up in the Dagster UI and runs on the defined cadence. This is another benefit of the layout of Dagster projects with `dg` autoloading all the objects in a project. This means less code the agent needs to write and be aware and less of chance for things to quietly get out of sync during development.
