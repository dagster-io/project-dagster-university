---
title: 'Lesson 5: Dagster objects'
module: 'dagster_testing'
lesson: '5'
---

The majority of your tests will involve assets as they comprise the majority of your organizational logic. You should not focus as much on testing the other Dagster objects in your outside of the definitions test just discussed. However here are some tips if you would like to test these objects in more detail.


## Jobs

Jobs are a collection of assets grouped together in a specific way. Generally these are used to run a subset of your asset graph in a predetermined way. Below are top jobs, both using the same subset of the graph though one also supplies a run configuration:

```python
partition_asset = dg.AssetSelection.assets("partition_asset")

my_job = dg.define_asset_job(
    name="jobs",
    selection=dg.AssetSelection.all() - partition_asset,
)


my_job_configured = dg.define_asset_job(
    name="jobs_config",
    selection=dg.AssetSelection.all() - partition_asset,
    config=yaml.safe_load(
        (Path(__file__).absolute().parent / "run_config.yaml").open()
    ),
)
```

As well as ensuring that the jobs exist and can access the aspects of the job itself. This allows you to write to tests to ensure parts of the job remain how we expect. For example the `my_job_configured` is configured by a yaml and maybe we want to always ensure that the number for the asset `config_asset` remains the same. 

```python
def test_job_config():
    assert jobs.my_job_configured.config["ops"]["config_asset"]["config"]["number"] == 10
```

## Schedules

Like jobs, schedules allow you to access the internals you set for the schedule you define.

```python
my_schedule = dg.ScheduleDefinition(
    name="my_schedule",
    job=jobs.my_job,
    cron_schedule="0 0 5 * *",
    run_config=dg.RunConfig({"config_asset": assets.AssetConfig(number=20)}),
)


def test_schedule():
    assert schedules.my_schedule
    assert schedules.my_schedule.cron_schedule == "0 0 5 * *"
    assert schedules.my_schedule.job == jobs.my_job
```

These validation tests can be useful on occasions when you need to ensure certain aspects but can generally be left out.

## Sensors

Custom sensors are one Dagster object were it might be worthwhile to include tests. For our example we have a simple sensor that checks for new files (though it does so based on `random.random()`) and then executes a run or skip based on the result: 

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

We may want to write a test to ensure the logic is behaving the way we expect. To do this with the way our sensor is written, we will go back to our lesson on mocking.

We want to patch and set the return value for the `check_for_new_files` function and ensure that our sensor acts accordingly.

First we can set a test where our sensor will skip:

```python
@patch("dagster_testing.lesson_5.sensors.check_for_new_files", return_value=[])
def test_sensor_skip(mock_check_new_files):
    instance = dg.DagsterInstance.ephemeral()
    context = dg.build_sensor_context(instance=instance)
    assert sensors.my_sensor(context).__next__() == dg.SkipReason("No new files found")
```

The code above:

1. Patches the `check_for_new_files` and sets a return value of an empty list
2. Initializes an ephemeral Dagster instance which is necessary when testing aspects of Dagster that use the daemon
3. Builds the sensor context using that instance
4. Executes the sensor. This returns a generator where we access the first element with `__next__()` and ensure it matches our `SkipReason`

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