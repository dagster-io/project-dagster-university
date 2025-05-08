---
title: "Lesson 3: Triggering partitions"
module: 'dagster_etl'
lesson: '3'
---

# Triggering partitions

The question of how to automate your pipelines largely depends on how your data arrives and how you want to respond to it. At a high level, there are two main strategies: scheduled and event-driven execution.

## Scheduled ETL
Scheduled ETL pipelines run at fixed intervals. This works well for data that arrives consistently — for example, if a file is uploaded every morning at 5:00 AM, you might schedule your ETL process to run at 5:15 AM, giving it a buffer to ensure the file has arrived.

Scheduling is a simple and common way to manage ETL. It's easy to set up, reliable in predictable environments, and integrates cleanly with most orchestration tools. However, it lacks nuance. What if the file arrives late — say at 5:45 AM? Unless you’ve implemented proper alerting, your pipeline might fail silently or generate errors. Even with alerts, you'd need to manually verify the file has arrived and trigger an ad-hoc run to process it.

## Event-driven ETL
Event-driven pipelines are triggered by a change in state — such as the arrival of a new file. In this model, the timing of the file’s arrival doesn’t matter (5:00 AM, 5:45 AM, 8:00 AM...). The event itself — the detection of a new file — is what triggers the pipeline.

This approach is more flexible and responsive, but it comes with additional complexity. You need a way to track state, so the system knows which files have already been processed and which ones are new. Without this, you risk duplicate processing or missed data.

The best way to understand the difference is to see it in action within Dagster. In fact, we’ve already set up our two partitioned pipelines to demonstrate both workflows:

One pipeline uses a schedule to process time-based partitions.

The other uses a sensor to react to file system events and drive dynamic partitions.

This contrast will give you a clear picture of how Dagster supports both scheduled and event-driven ETL, and when each approach is most appropriate.

## Implementing schedules

For our scheduled pipeline, we’ll use the assets associated with the `DailyPartitionsDefinition` partition. As a reminder, this partition definition requires a specific date (e.g., "2018-01-22") for the asset to execute.

Because we're using Dagster’s built-in `DailyPartitionsDefinition` class to generate a fixed pattern of daily partitions, Dagster can automatically create a corresponding schedule for us. All we need to do is provide the job we want to run and define the cadence at which it should run — for example, daily at a specific time. Dagster will then handle generating the appropriate partition key for each run.

This makes it simple to set up reliable, automated ETL for any use case where data arrives on a regular schedule:

```python
import dagster as dg

import dagster_and_etl.defs.jobs as jobs

asset_partitioned_schedule = dg.build_schedule_from_partitioned_job(
    jobs.import_partition_job,
    cron_schedule="0 6 * * *",
)
```

## Implementing Event-driven

As mentioned earlier, event-driven pipelines are a bit more complex because they require maintaining state — specifically, knowing which data has already been processed and which is new. The good news is that Dagster handles most of this complexity for you through an abstraction called sensors.

Sensors in Dagster allow you to monitor external systems — like cloud storage or APIs — and trigger pipeline runs when new data is detected. They are particularly useful when working with dynamic partitions, where the set of valid partition keys can change over time.

Here’s an example of what a sensor might look like for a dynamically partitioned asset using `s3_partitions_def`:

```python
import json
import os
from pathlib import Path

import dagster as dg

import dagster_and_etl.defs.jobs as jobs


@dg.sensor(target=jobs.import_dynamic_partition_job)
def dynamic_sensor(context: dg.SensorEvaluationContext):
    file_path = Path(__file__).absolute().parent / "../data/source/"

    previous_state = json.loads(context.cursor) if context.cursor else {}
    current_state = {}
    runs_to_request = []

    for filename in os.listdir(file_path):
        if filename not in previous_state:
            last_modified = os.path.getmtime(file_path)
            current_state[filename] = last_modified

            runs_to_request.append(
                dg.RunRequest(
                    run_key=filename,
                )
            )

    return dg.SensorResult(
        run_requests=runs_to_request, cursor=json.dumps(current_state)
    )
```

Event-driven pipelines can be more resilient and responsive, but they do come with some important considerations. First, you need access to the system where the state is being checked. In our example, this isn’t an issue since we’re monitoring the local file system. But what if the files lived in a remote system, like an S3 bucket, Azure Blob Storage, or a third-party FTP server?

In those cases, you’ll need appropriate credentials and potentially network access to query those systems regularly. You also need to ensure your sensor logic is efficient — especially when dealing with cloud resources, where frequent polling could result in increased costs or throttling. Despite these concerns, when implemented properly, event-driven pipelines can significantly reduce latency and manual intervention in your workflows.
