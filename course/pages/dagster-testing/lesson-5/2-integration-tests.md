---
title: 'Lesson 5: Integration tests'
module: 'dagster_testing'
lesson: '5'
---

# Integration tests

We can begin by defining a new asset similar to `state_population_file` that retrieves city population data from a database.

Assume a table exists in our production data warehouse, `data.city_population`, that contains all the different cities in all states. The table has the following schema.

| Name | Type | Description |
| --- | --- | --- |
| state_name | VARCHAR(100) | The name of the state |
| city_name | VARCHAR(100) | The name of the city |
| population | INT | The city population |

We will hardcode our asset to look for the cities in New York and return the results from Snowflake using a resource.

```python
@dg.asset
def state_population_database(database: SnowflakeResource) -> list[tuple]:
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

When we run this asset, we need to supply a Snowflake resource. The connection to Snowflake is defined with environmental variables when initializing the Snowflake resource and is set in the Definition for the resources.

```python
@dg.definitions
def resources():
    return dg.Definitions(
        resources={
            "database": snowflake_resource,
        },
    )
```

This is a good way to structure the code. We separate the application code from the configuration code in proper [Twelve-Factor](https://12factor.net/) fashion.

This means we could write an integration test that uses Snowflake but uses a different configuration to connect to a different database. Perhaps we have a staging database in our Snowflake account as well.

```python
def test_snowflake_staging():
    snowflake_staging_resource = SnowflakeResource(
        account=dg.EnvVar("SNOWFLAKE_ACCOUNT"),
        user=dg.EnvVar("SNOWFLAKE_USERNAME"),
        password=dg.EnvVar("SNOWFLAKE_PASSWORD"),
        database="STAGING",
        warehouse="STAGING_WAREHOUSE",
    )

    lesson_5.state_population_database(snowflake_staging_resource)
```

This is an integration test. We are executing our asset and ensuring it works with an actual connection to Snowflake. This is a good step but may not be what we always want for testing.

There are a few problems with doing integration tests like the one above. Because Snowflake is consumption based, it means we will have to pay a small amount every time we execute a test. Also since we are querying a cloud OLAP system there is no guarantee on the time the test might take. It might take only a second or two but it could take a minute depending on warehouse allocation. Finally this assumes there is an equivalent staging environment in Snowflake. Perhaps we do not have an staging database with similar data for testing.

One way to avoid these concerns is to maintain a separate environment just for integration tests. We will then need to substitute that connection into our asset. This is where Dagster can help and allow us to do some very interesting things with integration testing.
