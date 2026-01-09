---
title: "Lesson 3: Triggering partitions"
module: 'dagster_etl'
lesson: '3'
---

# Triggering partitions

The question of how to automate your pipelines largely depends on how your data arrives. At a high level, there are two main strategies: scheduled and event-driven execution.

## Scheduled ETL
Scheduled ETL pipelines run at fixed intervals. This works well for data that arrives consistently. For example, if a file is uploaded every morning at 5:00 AM, you might schedule your ETL process to run at 5:15 AM (supplying a small buffer).

Scheduling is a simple and very common with ETL. It's easy to set up, reliable, and integrates cleanly with most orchestration tools. However, it lacks nuance. What if the file arrives late, say at 5:45 AM? Unless you’ve implemented proper alerting, your pipeline might fail silently. Even with alerts, you'd need to manually verify when file has actually arrived and trigger an ad-hoc run to process it.

## Event-driven ETL
Event-driven pipelines are triggered by a change in state, such as the arrival of a new file itself. In this model, the timing of the file’s arrival doesn’t matter (5:00 AM, 5:45 AM, 8:00 AM...). The detecting a new file is what triggers the pipeline.

This approach is more flexible and responsive, but it comes with additional complexity. You need a way to track state, so the system knows which files have already been processed and which ones are new. Without this, you risk duplicate processing or missed data.

## Scheduling in Dagster

Our two partitioned pipelines can demonstrate the differences between these two strategies. The time-based partitioned assets fit a schedule while the dynamic partitioned assets will use a sensor (which is Dagster's way to handle event driven architectures).

## Implementing schedules

For our scheduled pipeline, we’ll use the assets associated with the `DailyPartitionsDefinition` partition. As a reminder, this partition definition requires a specific date (e.g., "2018-01-22") for the asset to execute.

Because we're using Dagster’s built-in `DailyPartitionsDefinition` class to generate a fixed pattern of daily partitions, Dagster can automatically create a corresponding schedule for us. All we need to do is provide the job we want to run and define the cadence at which it should run. Dagster will handle generating the appropriate partition key for each execution:

```python
import dagster as dg

import dagster_and_etl.defs.jobs as jobs

asset_partitioned_schedule = dg.build_schedule_from_partitioned_job(
    jobs.import_partition_job,
)
```

This makes it simple to set up reliable, automated ETL for any use case where data arrives on a regular schedule.

## Implementing Event-driven

As mentioned earlier, event-driven pipelines are a bit more complex because they require maintaining state, specifically knowing which data has already been processed and which is new. The good news is that Dagster handles most of the complexity around state management through an abstraction called sensors.

Sensors in Dagster allow you to monitor external systems, like cloud storage, and trigger pipeline runs when new data is detected. They are particularly useful when working with dynamic partitions, where the set of valid partition keys is not always known.

Here’s an example of what a sensor might look like for a dynamically partitioned asset. First we will define the job:

```python
# src/dagster_and_etl/defs/jobs.py
import dagster as dg

import dagster_and_etl.defs.assets as assets

import_dynamic_partition_job = dg.define_asset_job(
    name="import_dynamic_partition_job",
    selection=[
        assets.import_dynamic_partition_file,
        assets.duckdb_dynamic_partition_table,
    ],
)
```

Then we can define the sensor:

```python
# src/dagster_and_etl/defs/sensors.py
import json
import os
from pathlib import Path

import dagster as dg

import dagster_and_etl.defs.jobs as jobs
from dagster_and_etl.defs.assets import dynamic_partitions_def

@dg.sensor(target=jobs.import_dynamic_partition_job)
def dynamic_sensor(context: dg.SensorEvaluationContext) -> dg.SensorResult:
    file_path = Path(__file__).absolute().parent / "../../../data/source/"

    previous_state = json.loads(context.cursor) if context.cursor else {}
    current_state = {}
    runs_to_request = []
    dynamic_partitions_requests = []

    for filename in os.listdir(file_path):
        if filename not in previous_state:
            partition_key = filename.split(".")[0]
            last_modified = os.path.getmtime(file_path)
            current_state[filename] = last_modified

            dynamic_partitions_requests.append(partition_key)
            runs_to_request.append(
                dg.RunRequest(
                    run_key=filename,
                    partition_key=partition_key,
                )
            )

    return dg.SensorResult(
        run_requests=runs_to_request,
        cursor=json.dumps(current_state),
        dynamic_partitions_requests=[
            dynamic_partitions_def.build_add_request(dynamic_partitions_requests)
        ],
    )
```

The code above does the following:

1. Defines a sensor using the `dg.sensor` decorator for our `import_dynamic_partition_job` job.
2. Sets the current state from the `context` of the sensor. This determines the history of what the sensor has already processed.
3. Iterates through the files in the `data/sources` directory and determines if there are any new files since the last time the sensor ran.
4. Executes the `import_dynamic_partition_job` for any new files that have been added.

Now if we enable this sensor, it will trigger executions for all three files in the `data/sources` directory.

Event-driven pipelines like this can be more resilient and responsive, but they come with some important considerations.

First, you need access to the system where state is being checked. In our example, this isn’t an issue since we’re monitoring the local file system. But what if the files lived in a remote system where we don’t have full read access? That could limit our ability to detect changes reliably.

You also need to ensure that your sensor logic is efficient. For example, if you’re reading from an S3 bucket containing thousands of files, your sensor would need to query the entire bucket each time it runs. To mitigate this, it's often better to include logic that filters files by a specific prefix or folder path, reducing the scope of each scan.

Finally, consider what happens when a sensor is enabled for the first time. Because sensors typically detect anything that hasn’t already been processed, the initial run can trigger a large number of events, potentially attempting to process everything at once.
