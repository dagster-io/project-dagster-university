---
title: 'Lesson 4: Integration Tests'
module: 'dagster_testing'
lesson: '4'
---

We will define an asset that uses a `database` resource to execute a query against Snowflake:

```python
@dg.asset
def my_sql_table(database: SnowflakeResource):
    query = "SELECT * FROM information_schema.columns;"
    with database.get_connection() as conn:
        conn.cursor().execute(query)
```

In the `definitions.py` we define the Snowflake resource using environment variables like this:

```python
snowflake_resource = SnowflakeResource(
    account=dg.EnvVar("SNOWFLAKE_ACCOUNT"),
    user=dg.EnvVar("SNOWFLAKE_USERNAME"),
    password=dg.EnvVar("SNOWFLAKE_PASSWORD"),
    database=dg.EnvVar("SNOWFLAKE_DATABASE"),
    warehouse=dg.EnvVar("SNOWFLAKE_WAREHOUSE"),
)


defs = dg.Definitions(
    assets=[my_sql_table],
    resources={
        "database": snowflake_resource,
    },
)
```

Because we are storing the environment information separately from the application code in proper [Twelve-Factor](https://12factor.net/) fashion. We could do integration testing by providing different environment information when testing. Maybe this would connect to a different database in Snowflake and use a different warehouse.

This can help ensure we can run tests without the risk of using production systems. However this is still expensive. For our example we can actually do something more interesting.