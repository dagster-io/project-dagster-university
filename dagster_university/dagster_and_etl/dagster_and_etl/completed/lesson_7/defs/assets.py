import dagster as dg


@dg.asset
def postgres_customers():
    return "postgres://postgres:postgres@localhost:5432/postgres"
