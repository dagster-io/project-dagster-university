import json
import os
from pathlib import Path

import dagster as dg

import dagster_and_etl.completed.lesson_3.defs.jobs as jobs
from dagster_and_etl.completed.lesson_3.defs.assets import dynamic_partitions_def


@dg.sensor(target=jobs.import_dynamic_partition_job)
def dynamic_sensor(context: dg.SensorEvaluationContext) -> dg.SensorResult:
    file_path = Path(__file__).absolute().parent / "../../../../../data/source/"

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
