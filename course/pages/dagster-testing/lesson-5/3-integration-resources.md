---
title: 'Lesson 5: Integration resources'
module: 'dagster_testing'
lesson: '4'
---

# Integrations resources

If we think about the `state_population_database` asset, we want to make sure it can execute a query, but we are not necessarily concerned with which database is used to execute the query. Instead of insisting that the `database` resource must be Snowflake, we can change the annotation so that it can take in any resource:

```python
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
```

Now in order to execute the asset, we only need to provide a resource that has a `get_connection` context manager with methods for `cursor` and `execute`.  From Dagster's perspective, this does not even need to be a database. As long as it meets those criteria.

For our purposes we will create a resource that provides similar functionality but uses a different database. We will use Postgres which, unlike Snowflake, is open sourced and can be used for free and run on our local machine.

A benefit of using Postgres is that its Python client is a lot like the Snowflake Python client. Here is a resource to allow us to execute queries in Postgres. Click **View answer** to view it.

```python {% obfuscated="true" %}
class PostgresResource(dg.ConfigurableResource):
    user: str
    password: str
    host: str
    database: str

    def _connection(self):
        return psycopg2.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            database=self.database,
        )

    @contextmanager
    def get_connection(self):
        yield self._connection()
```

This resource provides everything we need and can be used in place of the Snowflake resource for the purposes of integration testing to ensure that our asset works while still connecting to a database.

## Similar resources

We defined our own Postgres resource to take the place of Snowflake but there are  other options. One popular tool is DuckDB which serves as an OLAP database that can run locally. This can serve as a great substitute for a data warehouse like Snowflake. Just remember that something like:

```python
@dg.asset
def truncate_table(database: dg.ConfigurableResource) -> None:
    query = "TRUNCATE TABLE data.city_population"
    with database.get_connection() as conn:
        conn.execute(query)
```

Would not work with Snowflake because Snowflake requires the cursor while DuckDB does not. The code would need to match for both resources:

```python
@dg.asset
def truncate_table(database: dg.ConfigurableResource) -> None:
    query = "TRUNCATE TABLE data.city_population"
    with database.get_connection() as conn:
        cur = conn.cursor() # Cursor is required
        cur.execute(query)
```