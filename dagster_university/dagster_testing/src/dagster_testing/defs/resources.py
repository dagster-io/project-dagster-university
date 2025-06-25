import dagster as dg


class StatePopulation(dg.ConfigurableResource):
    def get_cities(self, state: str) -> list[dict]:
        return [
            {
                "City": "Milwaukee",
                "Population": 577222,
            },
            {
                "City": "Madison",
                "Population": 269840,
            },
        ]


@dg.definitions
def resources():
    return dg.Definitions(
        resources={
            "state_population_resource": StatePopulation(),
            "database": dg.ResourceDefinition.mock_resource(),
        },
    )
