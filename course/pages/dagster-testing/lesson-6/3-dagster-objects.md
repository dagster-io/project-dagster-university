---
title: 'Lesson 6: Dagster objects'
module: 'dagster_testing'
lesson: '6'
---

# Testing other Dagster objects

The majority of your tests will involve assets as they comprise the majority of your organizational logic. You should not focus as much on testing the other Dagster objects with your tests outside of the definition test. However here are some tips if you would like to test the other Dagster objects in more detail.

## Jobs

Jobs are a collection of assets grouped together in a specific way. Generally these are used to run a subset of your asset graph in a predetermined way.

Here are two jobs, both using the same subset of the asset graph though `my_job_configured` also supplies a run configuration.

```python
state_population_file_partition = dg.AssetSelection.assets(
    "state_population_file_partition"
)
total_population_partition = dg.AssetSelection.assets("total_population_partition")


my_job = dg.define_asset_job(
    name="jobs",
    selection=dg.AssetSelection.all()
    - state_population_file_partition
    - total_population_partition,
)


my_job_configured = dg.define_asset_job(
    name="jobs_config",
    selection=dg.AssetSelection.all()
    - state_population_file_partition
    - total_population_partition,
    config=yaml.safe_load(
        (Path(__file__).absolute().parent / "run_config.yaml").open()
    ),
)
```

If we consider the aspects of our job we would like to test, most of it is the specifics we set such as the asset selection or the configuration. There is no need to write tests to ensure that jobs work as that is the responsibility of Dagster.

To test our jobs, we can write tests around their configurations by accessing elements of the object. For example, the `my_job_configured` is configured by a yaml and we might want to ensure that the asset is always using a certain file path.

```python
def test_job_config():
    assert (
        jobs.my_job_configured.config["ops"]["state_population_file_config"]["config"][
            "path"
        ]
        == "dagster_testing_tests/data/test.csv"
    )
```

Tests like this may not always be necessary but you may have Dagster projects where you need to ensure all aspects.

## Schedules

Like jobs, schedules allow you to access the internals of the object. Given a schedule like the following.

```python
my_schedule = dg.ScheduleDefinition(
    name="my_schedule",
    job=jobs.my_job,
    cron_schedule="0 0 5 * *",  # every 5th of the month at midnight
    run_config=dg.RunConfig(
        {
            "state_population_file_config": assets.FilepathConfig(
                path="dagster_testing_tests/data/test.csv"
            )
        }
    ),
)
```

You can write tests to check the cron syntax is correct or make sure it is using the correct job.

```python
def test_schedule():
    assert schedules.my_schedule
    assert schedules.my_schedule.cron_schedule == "0 0 5 * *"
    assert schedules.my_schedule.job == jobs.my_job
```

## Sensors

Custom sensors are one Dagster object were it might be worthwhile to include custom tests. Unlike jobs and schedules, sensors allow for far more customization and we may need to ensure that they trigger as expected.

For our example we have a simple sensor that checks for new files (though it does so based on `random.random()` for the purposes of this lesson) and executes a run or skip based on the result.

```python
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
```

A good test for this sensor would be to check that it does indeed trigger when a new file is present and does not trigger if no new files are found. To do that we need to see what the main trigger logic is. In this case it is when new files are returned by the `check_for_new_files` function.

In order to write a reliable test for this sensor, we will go back to our lesson on mocking. We want to patch and set the return value for the `check_for_new_files` function to ensure when new files are and are not produced.

First we can set a test where our sensor will skip.

```python
@patch("dagster_testing.lesson_5.sensors.check_for_new_files", return_value=[])
def test_sensor_skip(mock_check_new_files):
    instance = dg.DagsterInstance.ephemeral()
    context = dg.build_sensor_context(instance=instance)
    assert sensors.my_sensor(context).__next__() == dg.SkipReason("No new files found")
```

The code above:

1. Patches `check_for_new_files` and sets a return value of an empty list.
2. Initializes an ephemeral Dagster instance which is necessary when testing aspects of Dagster that use the daemon.
3. Builds the sensor context using that instance.
4. Executes the sensor. This returns a generator where we access the first element with `__next__()` and ensure it matches our `SkipReason`.

What would it look like to write a test to ensure the sensor picks up a new file? Click **View answer** to view it.

```python {% obfuscated="true" %}
@patch(
    "dagster_testing.lesson_5.sensors.check_for_new_files", return_value=["test_file"]
)
def test_sensor_run(mock_check_new_files):
    instance = dg.DagsterInstance.ephemeral()
    context = dg.build_sensor_context(instance=instance)
    assert sensors.my_sensor(context).__next__() == dg.RunRequest(run_key="test_file")
```