import json
import os
from pathlib import Path

import dagster as dg

import src.dagster_and_etl.completed.lesson_3.defs.jobs as jobs


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
