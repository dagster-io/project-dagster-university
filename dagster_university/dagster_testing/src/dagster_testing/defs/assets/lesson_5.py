import dagster as dg
from pandas import DataFrame, Series

# Integration test assets


@dg.asset
def state_population_database(database: dg.ConfigurableResource) -> list[tuple]:
    query = """
        SELECT
            city_name,
            population
        FROM data.city_population
        WHERE state_name = 'NY';
    """
    with database.get_connection() as conn:
        cur = conn.cursor()
        cur.execute(query)
        return cur.fetchall()


class StateConfig(dg.Config):
    name: str


@dg.asset
def total_population_database(state_population_database: list[tuple]) -> int:
    return sum(value for _, value in state_population_database)


# Smoke test assets


raw_country_populations = dg.SourceAsset(
    key="raw_country_populations",
    metadata={
        "column_schema": dg.TableSchema.from_name_type_dict(
            {
                "country": "string",
                "continent": "string",
                "pop2023": "int64",
                "pop2024": "int64",
                "change": "float64",
            }
        ),
    },
)


@dg.asset
def country_populations(raw_country_populations: DataFrame) -> DataFrame:
    df = raw_country_populations.copy()
    df["growth"] = df["pop2024"] - df["pop2023"]
    return df


@dg.asset
def continent_stats(country_populations: DataFrame) -> DataFrame:
    return country_populations.groupby("continent").agg(
        {"pop2024": "sum", "change": "mean"}
    )


# Smoke test utilities


def empty_dataframe_from_schema(column_schema: dg.TableSchema) -> DataFrame:
    return DataFrame(
        {col.name: Series(dtype=col.type) for col in column_schema.columns}
    )


class SmokeIOManager(dg.InMemoryIOManager):
    def load_input(self, context: dg.InputContext):
        if context.upstream_output is not None:
            column_schema = context.upstream_output.metadata.get("column_schema")
            if column_schema:
                return empty_dataframe_from_schema(column_schema)

        return super().load_input(context)
