---
title: 'Lesson 4: Integration tests'
module: 'dagster_testing'
lesson: '4'
---

First we will define an asset that connects to a database via a resource and queries the information schema (metadata about the tables and columns contained with the database).

```python
@dg.asset
def my_sql_table(database: SnowflakeResource):
   query = "SELECT * FROM information_schema.columns;"
   with database.get_connection() as conn:
       conn.cursor().execute(query)
```

Imagine that in production, this asset connects to our Snowflake data warehouse. The connection to Snowflake is defined with environmental variables when initializing the Snowflake resource and is set in the definitions:

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

Because we separate our application code from the configuration code in proper [Twelve-Factor](https://12factor.net/) fashion. We could do integration testing by providing different environment information to point to a different Snowflake database.

```python
@pytest.mark.skip
def test_snowflake_staging():
   snowflake_staging_resource = SnowflakeResource(
       account=dg.EnvVar("SNOWFLAKE_ACCOUNT"),
       user=dg.EnvVar("SNOWFLAKE_USERNAME"),
       password=dg.EnvVar("SNOWFLAKE_PASSWORD"),
       database="STAGING",
       warehouse="STAGING_WAREHOUSE",
   )

   my_sql_table(snowflake_staging_resource)
```

This test would still use Snowflake to execute but would not connect to the production database data or use production compute.

This is a good step but we do not always want to run queries against Snowflake as that may start to get expensive. Using Dagster we can actually do something much more interesting instead.
