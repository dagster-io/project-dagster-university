
from dagster import (
    RunRequest,
    SkipReason,
    sensor,
    make_email_on_run_failure_sensor,
)
import os
import json

from ..jobs import adhoc_request_job

# recipient_string = os.getenv("ALERT_EMAIL_RECIPIENTS", "")
# recipients = recipient_string.split(",")

# NOTE: This doesn't work anymore because Google has disabled the ability to send emails from "less secure apps".
# By default, tries connecting to GMail. See the docs for more info about connecting via SMTP:
# https://docs.dagster.io/_apidocs/utilities#dagster.make_email_on_run_failure_sensor
# on_global_failure_sensor = make_email_on_run_failure_sensor(
#     email_subject_fn=lambda context: "Job failed!",
#     email_from=os.getenv("ALERT_EMAIL_FROM", ""),
#     email_to=recipients,
#     email_password=os.getenv("ALERT_EMAIL_PASSWORD", ""),
# )

@sensor(
    job=adhoc_request_job
)
def adhoc_request_sensor(context):
    PATH_TO_REQUESTS = os.path.join(os.path.dirname(__file__), "../../", "data/requests")

    previous_state = json.loads(context.cursor) if context.cursor else {}
    current_state = {}
    to_request = []

    for filename in os.listdir(PATH_TO_REQUESTS):
        file_path = os.path.join(PATH_TO_REQUESTS, filename)
        if filename.endswith(".json") and os.path.isfile(file_path):
            last_modified = os.path.getmtime(file_path)
            
            current_state[filename] = last_modified

            # if the file is new or has been modified since the last run, add it to the request queue
            if filename not in previous_state or previous_state[filename] != last_modified:
                to_request.append((filename, last_modified))
    
    # json the new state and update the cursor
    context.update_cursor(json.dumps(current_state))

    if len(to_request) == 0:
        yield SkipReason("No new requests to process.")

    # loop through the files to request and yield a run request for each
    for request in to_request:
        with open(os.path.join(PATH_TO_REQUESTS, request[0]), "r") as f:
            request_config = json.load(f)

        yield RunRequest(
            run_key=f"adhoc_request_{request[0]}_{request[1]}",
            run_config={
                "ops": {
                    "adhoc_request": {
                        "config": {
                            "filename": request[0],
                            **request_config
                        }
                    }
                }
            }
        )