import dagster as dg

from dagster_essentials.completed.lesson_7.assets import metrics, trips
from dagster_essentials.completed.lesson_7.definitions import defs
from dagster_essentials.completed.lesson_7.jobs import (
    trip_update_job,
    weekly_update_job,
)
from dagster_essentials.completed.lesson_7.resources import database_resource
from dagster_essentials.completed.lesson_7.schedules import (
    trip_update_schedule,
    weekly_update_schedule,
)


def test_assets():
    assets = [
        trips.taxi_trips_file,
        trips.taxi_zones_file,
        trips.taxi_trips,
        trips.taxi_zones,
        metrics.trips_by_week,
        metrics.manhattan_stats,
        metrics.manhattan_map,
    ]
    result = dg.materialize(
        assets=assets,
        resources={
            "database": database_resource,
        },
    )
    assert result.success


def test_jobs():
    assert trip_update_job.name == "trip_update_job"
    assert (
        trip_update_job.selection
        == dg.AssetSelection.all() - dg.AssetSelection.assets("trips_by_week")
    )
    assert weekly_update_job.name == "weekly_update_job"
    assert weekly_update_job.selection == dg.AssetSelection.assets("trips_by_week")


def test_schedules():
    assert trip_update_schedule.cron_schedule == "0 0 5 * *"
    assert trip_update_schedule.job == trip_update_job
    assert weekly_update_schedule.cron_schedule == "0 0 * * 1"
    assert weekly_update_schedule.job == weekly_update_job


def test_def_can_load():
    assert defs
    assert defs.get_job_def("trip_update_job")
    assert defs.get_job_def("weekly_update_job")
    assert defs.get_schedule_def("trip_update_job_schedule")
    assert defs.get_schedule_def("weekly_update_job_schedule")
