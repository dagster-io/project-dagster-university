import csv
from pathlib import Path

import dagster as dg

import dagster_testing.defs.resources as resources


class FilepathConfig(dg.Config):
    path: str


@dg.asset
def population_file_config(config: FilepathConfig) -> list[dict]:
    with open(config.path) as file:
        reader = csv.DictReader(file)
        return [row for row in reader]


@dg.asset
def population_api_resource(
    state_population_resource: resources.StatePopulation,
) -> list[dict]:
    return state_population_resource.get_cities("wi")


@dg.asset
def population_combined(
    population_file_config: list[dict],
    population_api_resource: list[dict],
) -> int:
    all_assets = population_file_config + population_api_resource
    return sum([int(x["Population"]) for x in all_assets])


@dg.asset_check(asset=population_combined)
def non_negative(population_combined):
    return dg.AssetCheckResult(
        passed=bool(population_combined > 0),
    )


# Blocking asset check - prevents downstream materialization on failure
@dg.asset_check(asset=population_file_config, blocking=True)
def validate_schema(population_file_config: list[dict]) -> dg.AssetCheckResult:
    """Block downstream processing if schema is invalid."""
    required_columns = {"City", "Population"}
    actual_columns = (
        set(population_file_config[0].keys()) if population_file_config else set()
    )

    passed = required_columns.issubset(actual_columns)

    return dg.AssetCheckResult(
        passed=passed,
        metadata={
            "required_columns": list(required_columns),
            "actual_columns": list(actual_columns),
        },
    )


# Asset check with severity levels
@dg.asset_check(asset=population_file_config)
def row_count_check(population_file_config: list[dict]) -> dg.AssetCheckResult:
    row_count = len(population_file_config)

    if row_count == 0:
        return dg.AssetCheckResult(
            passed=False,
            severity=dg.AssetCheckSeverity.ERROR,
            metadata={"row_count": 0},
        )
    elif row_count < 3:
        return dg.AssetCheckResult(
            passed=True,  # Warning, not failure
            severity=dg.AssetCheckSeverity.WARN,
            metadata={"row_count": row_count, "message": "Low row count"},
        )
    else:
        return dg.AssetCheckResult(
            passed=True,
            metadata={"row_count": row_count},
        )


# Multi-asset check - run multiple checks in a single execution
@dg.multi_asset_check(
    specs=[
        dg.AssetCheckSpec(name="has_cities", asset="population_file_config"),
        dg.AssetCheckSpec(name="has_populations", asset="population_file_config"),
    ]
)
def population_data_checks(population_file_config: list[dict]):
    """Run multiple checks in a single execution."""
    # Check that all rows have City
    missing_cities = sum(1 for row in population_file_config if not row.get("City"))

    yield dg.AssetCheckResult(
        check_name="has_cities",
        passed=missing_cities == 0,
        metadata={"missing_count": missing_cities},
    )

    # Check that all rows have Population
    missing_populations = sum(
        1 for row in population_file_config if not row.get("Population")
    )

    yield dg.AssetCheckResult(
        check_name="has_populations",
        passed=missing_populations == 0,
        metadata={"missing_count": missing_populations},
    )


# Factory pattern for generating asset checks
def create_not_null_check(asset_name: str, column: str):
    """Factory to create not-null checks for any column."""

    @dg.asset_check(asset=asset_name, name=f"{column}_not_null")
    def check_fn(asset_value: list[dict]) -> dg.AssetCheckResult:
        null_count = sum(1 for row in asset_value if row.get(column) is None)
        return dg.AssetCheckResult(
            passed=null_count == 0,
            metadata={"null_count": null_count, "column": column},
        )

    return check_fn


# Generate checks using the factory
city_not_null_check = create_not_null_check("population_file_config", "City")
population_not_null_check = create_not_null_check(
    "population_file_config", "Population"
)


file_partitions = dg.StaticPartitionsDefinition(["ca.csv", "mn.csv", "ny.csv"])


@dg.asset(partitions_def=file_partitions)
def population_file_partition(context: dg.AssetExecutionContext) -> list[dict]:
    file_path = Path(__file__).absolute().parent / f"../data/{context.partition_key}"

    with open(file_path) as file:
        reader = csv.DictReader(file)
        return [row for row in reader]


@dg.asset
def total_population_partition(population_file_partition: list[dict]) -> int:
    return sum([int(x["Population"]) for x in population_file_partition])


@dg.asset
def squared(number: int):
    return number * number


@dg.asset(key=["target", "main", "square_key"])
def squared_key(number: int):
    return number * number
