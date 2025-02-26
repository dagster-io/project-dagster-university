---
title: 'Lesson 5: Integration tests'
module: 'dagster_testing'
lesson: '4'
---

# Integration tests

First we will define an asset that connects to a database via a resource and queries a `data.city_population` table. This table contains all the different cities in all states with the following schema.

| Name | Type | Description |
| --- | --- | --- |
| state_name | VARCHAR(100) | The name of the state |
| city_name | VARCHAR(100) | The name of the city |
| population | INT | The city population |

To start with we will just hardcode our asset to look for the cities in New York and return the results from Snowflake:

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

When we run this asset, we need to supply a Snowflake resource. The connection to Snowflake is defined with environmental variables when initializing the Snowflake resource and is set in the definitions:

```python
all_assets = dg.load_assets_from_modules([assets])


snowflake_resource = SnowflakeResource(
    account=dg.EnvVar("SNOWFLAKE_ACCOUNT"),
    user=dg.EnvVar("SNOWFLAKE_USERNAME"),
    password=dg.EnvVar("SNOWFLAKE_PASSWORD"),
    warehouse=dg.EnvVar("SNOWFLAKE_WAREHOUSE"),
)


defs = dg.Definitions(
    assets=all_assets,
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

    assets.state_population_database(snowflake_staging_resource)
```

This is an integration test. We are ensuring our asset works by connecting to a database. This is a good step but may not be what we always want to do for testing. In some cases you may not have an equivalent staging environment. Or you may not want to use an expensive system to execute against. 

We may want to use a live service for testing but not necessarily the system we are using in production. This is where Dagster can help and allows us to do some very interesting integration testing.
