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
