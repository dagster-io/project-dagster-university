---
title: "Lesson 3: Triggering partitions"
module: 'dagster_etl'
lesson: '3'
---

# Triggering partitions

The question of how to automate your pipelines is dependent on how your data and how you react to it. At a high level there are two main choices, scheduled and event-driven.

Scheduled ETL executes at fixed intervals. This works well for data that arrives at similar fixed intervals. For example if we know a file will be uploaded each morning at 5am, we can schedule our ETL process at 5:15am (including an extra buffer to be safe) to run.

Handling ETL with schedules is common because it is very easy to configure and maintain. Though it is not a very nuanced way to handle ETL. What happens if our file comes in at 5:45am? If we have proper alerting we would be notified that our pipeline did not run successfully. We would then have to manually check to see when the file has been uploaded and then trigger an adhoc run to ingest that file.

The opposite of scheduled pipelines are event-driven. In an event-driven pipeline, the triggering event is a change in state. This can be any number of things. But keeping with our file example, the triggering event would be when the file itself is added. In an event-driven workflow it would not matter when the file is added (5am, 5:45am, 8am...), the event of a new file being added triggers our pipeline.

This is helpful but adds complexity. In order to determine what the new file is, there has to be some way to retain the state of what files have already been processed.

The best way to see this difference is going back into Dagster. We have actually set up our two partitioned pipelines to work with each of these different workflows.

## Scheduled

For our scheduled pipeline we will use the assets associated with the `DailyPartitionsDefinition` partition. If we remember that partition requires a date (like "2018-01-22") for the asset to execute.

Because we are using the Dagster class `DailyPartitionsDefinition` to generate the fixed pattern of a daily partition, we can have Dagster automatically generate a schedule for us. All we have to do is supply our job and the schedule we would like our job to run on:

```python
import dagster as dg

import dagster_and_etl.defs.jobs as jobs

asset_partitioned_schedule = dg.build_schedule_from_partitioned_job(
    jobs.import_partition_job,
    cron_schedule="0 6 * * *",
)
```

## Event-driven

We mentioned that event-driven pipelines are a little more complicated because they require us to maintain state. The good news is that Dagster can handle most of the hard work around this. In Dagster we use the abstraction of sensors to check for changes in an external source.

Here is what a sensor would look like for the dynamically partitioned `s3_partitions_def`

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

Event-driven pipelines can be more resilient but they do have some considerations. First of all you need to have some degree of access to where state is checked. For our example this is not a problem since we are just checking our local file system. But what if the files existed in a  