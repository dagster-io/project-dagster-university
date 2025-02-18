import dagster as dg


@dg.asset
def my_sql_table(database: dg.ConfigurableResource):
    query = "SELECT * FROM information_schema.columns;"
    with database.get_connection() as conn:
        conn.cursor().execute(query)
