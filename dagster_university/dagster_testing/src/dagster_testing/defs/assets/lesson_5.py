import dagster as dg


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
