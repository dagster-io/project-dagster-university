import random

import dagster as dg

import dagster_testing.lesson_5.jobs as jobs


def check_for_new_files() -> list[str]:
    if random.random() > 0.5:
        return ["file1", "file2"]
    return []


@dg.sensor(
    name="my_sensor",
    job=jobs.my_job_configured,
    minimum_interval_seconds=5,
)
def my_sensor():
    new_files = check_for_new_files()
    # New files, run `my_job`
    if new_files:
        for filename in new_files:
            yield dg.RunRequest(run_key=filename)
    # No new files, skip the run and log the reason
    else:
        yield dg.SkipReason("No new files found")
