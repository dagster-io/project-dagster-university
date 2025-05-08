---
title: "Lesson 4: Triggering API jobs"
module: 'dagster_etl'
lesson: '4'
---

# Triggering API jobs

This development is following the same pattern as the previous lesson. We have a pipeline that we are able to run ad hoc to load data into DuckDB. Though we may want to automate this.

Given that everything we have built is time based and revolves around daily extracts, a schedule would be the best option to automate this process.

Let's create a schedule for this pipeline. First we can create a simple job for the three assets in this pipeline:

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

We will use this job in the schedule. The first question we need to ask is when to execute the schedule. Because the assets will get run for the previous day, we can aim to run it in the morning, let's say 6am. We don't want to run the pipeline too close to midnight to make sure the data has time to update, though like all things when designing around APIs, you will want to learn the specific details.

This schedule will look similar to our previous schedules except when the schedule executes, it will need to supply a run configuration to the job. Luckily we can use the execution time from the schedule itself to initialize the run configuration.

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