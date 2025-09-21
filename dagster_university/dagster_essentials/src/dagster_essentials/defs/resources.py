from dagster_duckdb import DuckDBResource
import dagster as dg

database_resource = DuckDBResource(
    database=dg.EnvVar("DUCKDB_DATABASE")      # replaced with environment variable
)

@dg.definitions
def resources():
    return dg.Definitions(resources={"database": database_resource})