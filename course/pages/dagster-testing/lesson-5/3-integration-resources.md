---
title: 'Lesson 5: Integration resources'
module: 'dagster_testing'
lesson: '4'
---

# Integrations resources

If we think about the `state_population_database` asset, we want to make sure it can execute a query, but we are not necessarily concerned with which database is used to execute the query. Instead of insisting that the `database` resource must be Snowflake, we can change the annotation so that it can take in any resource:

```python
@dg.asset
def my_sql_table(database: dg.ConfigurableResource):
    query = "SELECT * FROM information_schema.columns;"
    with database.get_connection() as conn:
        conn.cursor().execute(query)
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
@asset
def iris_dataset(duckdb: DuckDBResource) -> None:
    iris_df = pd.read_csv(
        "https://docs.dagster.io/assets/iris.csv",
        names=[
            "sepal_length_cm",
            "sepal_width_cm",
            "petal_length_cm",
            "petal_width_cm",
            "species",
        ],
    )

    with duckdb.get_connection() as conn:
        conn.execute("CREATE TABLE iris.iris_dataset AS SELECT * FROM iris_df")
```

Would not work with Snowflake because Snowflake requires the cursor while DuckDB does not. The code would need to match for both resources:

```python
@asset
def iris_dataset(duckdb: DuckDBResource) -> None:
    iris_df = pd.read_csv(
        "https://docs.dagster.io/assets/iris.csv",
        names=[
            "sepal_length_cm",
            "sepal_width_cm",
            "petal_length_cm",
            "petal_width_cm",
            "species",
        ],
    )

    with duckdb.get_connection() as conn:
        # Include cursor
        conn.cursor().execute("CREATE TABLE iris.iris_dataset AS SELECT * FROM iris_df")
```