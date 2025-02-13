import dagster as dg


class PostgresResource(dg.ConfigurableResource):
    def get_connection(self):
        pass

    @property
    def cursor(self):
        return self.connection.cursor()

    def execute(self, query):
        with self.connection.cursor() as cursor:
            cursor.execute(query)


@dg.asset
def my_table(database: dg.ConfigurableResource):
    with database.get_connection() as conn:
        query = "SELECT * FROM table"
        conn.execute(query)
