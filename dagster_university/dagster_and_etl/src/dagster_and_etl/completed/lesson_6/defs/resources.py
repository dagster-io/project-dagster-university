import dagster as dg
from dagster_sling import SlingConnectionResource, SlingResource

source = SlingConnectionResource(
    name="MY_POSTGRES",
    type="postgres",
    host="localhost",
    port=5432,
    database="test_db",
    user="test_user",
    password="test_pass",
)


destination = SlingConnectionResource(
    name="MY_DUCKDB",
    type="duckdb",
    connection_string="duckdb:///var/tmp/duckdb.db",
)

sling = SlingResource(
    connections=[
        source,
        destination,
    ]
)


@dg.definitions
def resources():
    return dg.Definitions(
        resources={
            "sling": sling,
        },
    )
