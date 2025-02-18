---
title: 'Lesson 4: Integration Resources'
module: 'dagster_testing'
lesson: '4'
---

If we think about the `my_sql_table` asset, we want to make sure it can execute a query, but we are less concerned with which database is used to execute the query. Instead of insisting that the `database` resource must be Snowflake, we can change the annotation so to just require a resource:

```python
@dg.asset
def my_sql_table(database: dg.ConfigurableResource):
    query = "SELECT * FROM information_schema.columns;"
    with database.get_connection() as conn:
        conn.cursor().execute(query)
```

Now we just need to provide a resource that has a method `get_connection` as a context manager and methods for `cursor` and `execute`.  From Dagster's perspective, this does not even need to be a database. As long as it meets the criteria so the asset can execute.

For our purposes we will create a resource that provides the same functionality but uses a different database. We will use Postgres which, unlike Snowflake, is open sourced and can be used for free. Also the Postgres Python client behaves similar to the Snowflake Python client. Click **View answer** to view it.

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

This resource provides everything we need and can be used in place of Snowflake to ensure our query executes against an actual database.

The final piece will be writing a test that uses Postgres instead of Snowflake.

## Similar resources

When thinking about using other resources, think in terms of the resource methods more than anything else. For example you may wanted to use DuckDB and the native Dagster DuckDB resource, you would need to use the `cursor`.