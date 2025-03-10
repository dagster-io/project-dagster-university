import dagster as dg
import requests

API_URL = "https://fake.com/population.json"


# This asset will fail as the API does not exist
@dg.asset
def state_population_api() -> list[dict]:
    output = []
    try:
        response = requests.get(API_URL, params={"state": "ny"})
        response.raise_for_status()

        for doc in response.json().get("cities"):
            output.append(
                {
                    "city": doc.get("city_name"),
                    "population": doc.get("city_population"),
                }
            )

        return output

    except requests.exceptions.RequestException:
        return output


class StatePopulation(dg.ConfigurableResource):
    def get_cities(self, state: str) -> list[dict]:
        output = []
        try:
            response = requests.get(API_URL, params={"state": state})
            response.raise_for_status()

            for doc in response.json().get("cities"):
                output.append(
                    {
                        "city": doc.get("city_name"),
                        "population": doc.get("city_population"),
                    }
                )

            return output

        except requests.exceptions.RequestException:
            return output


@dg.asset
def state_population_api_resource(
    state_population_resource: StatePopulation,
) -> list[dict]:
    return state_population_resource.get_cities("ny")


class StateConfig(dg.Config):
    name: str


@dg.asset
def state_population_api_resource_config(
    config: StateConfig, state_population_resource: StatePopulation
) -> list:
    return state_population_resource.get_cities(config.name)


# Downstream assets
@dg.asset
def total_population_resource(state_population_api_resource: list[dict]) -> int:
    return sum([x["population"] for x in state_population_api_resource])


@dg.asset
def total_population_resource_config(
    state_population_api_resource_config: list[dict],
) -> int:
    return sum([x["population"] for x in state_population_api_resource_config])
