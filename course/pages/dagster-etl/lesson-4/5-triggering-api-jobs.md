---
title: "Lesson 4: Triggering API jobs"
module: 'dagster_etl'
lesson: '4'
---

# Triggering API jobs

This development is following the same pattern as the previous lesson, we’ve built a pipeline that can be run ad hoc to load data into DuckDB. However, in many cases, we’ll want to automate this process to keep data up to date without manual intervention.

Since everything we’ve built so far is time-based and revolves around daily extracts, using a schedule is the most appropriate way to automate the pipeline.

Let’s start by creating a simple job that includes the three assets we’ve defined in this pipeline. Once the job is in place, we’ll attach a daily schedule to trigger it automatically:

```python
asteroid_job = dg.define_asset_job(
    name="asteroid_job",
    selection=[
        assets.asteroids,
        assets.asteroids_file,
        assets.duckdb_table,
    ],
)
```

We’ll use the job we just defined in our schedule. The first question to answer is when the schedule should execute. Since our assets are designed to process data for the previous day, it makes sense to run the schedule early in the morning, once the day has fully passed, let’s say around 6:00 AM.

We avoid running the pipeline too close to midnight to ensure the data has had time to fully populate. As with all API-based workflows, you’ll want to understand the behavior and latency of your specific source system before finalizing this timing.

This schedule will be similar to those we’ve written previously, with one key difference: it needs to supply a run configuration to the job. Fortunately, Dagster provides access to the execution time of the schedule, which we can use to dynamically generate the date for the run configuration.

Add the following schedule to the `schedules.py`:

```python
@dg.schedule(job=asteroid_job, cron_schedule="0 6 * * *")
def date_range_schedule(context):
    scheduled_date = context.scheduled_execution_time.strftime("%Y-%m-%d")

    return dg.RunRequest(
        run_config={
            "ops": {
                "asteroids": {
                    "config": {
                        "date": scheduled_date,
                    },
                },
            },
        },
    )
```

Now the pipeline is automated and will run every morning at fetch the previous days data.