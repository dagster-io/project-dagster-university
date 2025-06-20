---
title: 'Lesson 6: Setting up a database resource'
module: 'dagster_essentials'
lesson: '6'
---

# Setting up a database resource

Throughout this module, you’ve used DuckDB to store and transform your data. Each time you’ve used DuckDB in an asset, you’ve needed to make a connection to it. For example:

```python
@dg.asset(
    deps=["taxi_trips_file"],
)
def taxi_trips() -> None:
    ...
    conn = backoff(
        fn=duckdb.connect,
        retry_on=(RuntimeError, duckdb.IOException),
        kwargs={
            "database": os.getenv("DUCKDB_DATABASE"),
        },
        max_retries=10,
    )
    ...
```

Every asset that queries DuckDB contains the `duckdb.connect` line. As previously mentioned, this can become brittle and error-prone as your project grows, whether in the number of assets that use it or the complexity of the connections. For example, to MotherDuck, a specific S3 bucket, or loading an extension. To be exact, this brittleness is shared across the following assets:

- `taxi_zones`
- `taxi_trips`
- `manhattan_stats`
- `trips_by_week`

Let’s use a Dagster resource to manage this connection and share it across all the assets using it.

---

## Defining a resource

We can scaffold our resources with `dg` in a way similar to the how we scaffolded assets in lesson 3.

```bash
dg scaffold defs dagster.resources resources.py
```

This adds a `resources.py` file within the `dagster_essentials` module.

```
.
└── src
    └── dagster_essentials
        └── defs
            └── resources.py
```

Within this newly created file, add the following code:

```python
from dagster_duckdb import DuckDBResource


database_resource = DuckDBResource(
    database="data/staging/data.duckdb"
)
```

This code snippet imports a resource called `DuckDBResource` from Dagster’s `dagster_duckdb` integration library. Next, it creates an instance of that resource and stores it in `database_resource`.

---

## Using environment variables

When working across different settings or with secure values like passwords, environment variables are a standardized way to store configurations and credentials. Not specific to Python, environment variables are values that are saved outside of software and used within it. For a primer on environment variables in Python, check out [this post from our blog](https://dagster.io/blog/python-environment-variables).

When configuring resources, it’s best practice to load your configurations and secrets into your programs from environment variables. You’ve been following this pattern by using `os.getenv` to fetch environment variables from the `.env` that is part of this project. A `.env` file is a standard for project-level environment variables and should **not** be committed to git, as they often contain passwords and sensitive information.

However, in this project, our `.env` file only contains one environment variable: `DUCKDB_DATABASE`. This variable contains the hard-coded path to the DuckDB database file, which is `data/staging/data.duckdb`. Let’s clean up this code by using Dagster’s `EnvVar` utility.

In `resources.py`, replace the value of the `database` with an `EnvVar` as shown below:

```python
from dagster_duckdb import DuckDBResource
import dagster as dg

database_resource = DuckDBResource(
    database=dg.EnvVar("DUCKDB_DATABASE")      # replaced with environment variable
)
```

`EnvVar` is similar to the `os.getenv` method that you’ve been using, but there is a key difference:

- `EnvVar` fetches the environmental variable’s value **every time a run starts**
- `os.getenv` fetches the environment variable **when the code location is loaded**

By using `EnvVar` instead of `os.getenv`, you can dynamically customize a resource’s configuration. For example, you can change which DuckDB database is being used without having to restart Dagster’s web server.

---

## Updating the Definitions object

In the previous lesson, you learned about code locations, how they work, and how to collect assets and other Dagster definitions using the `Definitions` object.

You saw that using `dg` to scaffold our project, the `Definitions` will automatically load any assets within the module. The same is true for resources however there is one additional step we need to make to the `resources.py`.

1. In the `resources.py` add the following line:

   ```python
   @dg.definitions
   def resources():
       return dg.Definitions(resources={"database": database_resource})
   ```

   This tells Dagster how to map the resources to specific key names. In this case the `database_resource` resource just defined is mapped to the key name `database`.

2. In the Dagster UI, click **Deployment.**

3. In the **Code locations** tab, click the **Reload** button next to the `dagster_essentials` code location.

4. Click the code location to open it.

5. In the code location page that displays, click the **Definitions tab.**.

6. Click **Resources** on the left side panel and select the resource named **database**.

   Notice that the **Uses** tabe at the top is currently **0.** This is because while the resource has been defined and loaded, none of the assets in the code location are currently using it.

Now that you've set up the resource, it's time to use it in your project. In the next section, you'll learn how to refactor your assets to use resources.
