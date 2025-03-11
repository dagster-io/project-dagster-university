import dagster as dg

import dagster_testing.assets.dagster_assets as dagster_assets
import dagster_testing.assets.integration_assets as integration_assets
import dagster_testing.assets.mock_assets as mock_assets
import dagster_testing.assets.unit_assets as unit_assets
import dagster_testing.jobs as jobs
import dagster_testing.resources as resources
import dagster_testing.schedules as schedules
import dagster_testing.sensors as sensors

_unit_assets = dg.load_assets_from_modules([unit_assets])
_mock_assets = dg.load_assets_from_modules([mock_assets])
_integration_assets = dg.load_assets_from_modules([integration_assets])
_dagster_assets = dg.load_assets_from_modules([dagster_assets])


defs = dg.Definitions(
    assets=_unit_assets + _mock_assets + _integration_assets + _dagster_assets,
    asset_checks=[dagster_assets.non_negative],
    jobs=[jobs.my_job, jobs.my_job_configured],
    resources={
        "state_population_resource": resources.StatePopulation(),
        "database": dg.ResourceDefinition.mock_resource(),
    },
    schedules=[schedules.my_schedule],
    sensors=[sensors.my_sensor],
)
