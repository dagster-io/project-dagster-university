---
title: "Lesson 3: File import"
module: 'dagster_etl'
lesson: '3'
---

# File import

As mentioned, we’ll start by loading a file into a data warehouse. While we’re using a local file and a local DuckDB instance for simplicity, the same principles apply regardless of the source and destination. You could easily adapt this pipeline to pull data from another storage layer and load it into a different data warehouse.

## Config

Let’s consider the first asset we need. As we discussed, the logical approach to designing ETL pipelines is to start as far left in the diagram as possible and follow the data as it progresses through our system.

If we’re building a pipeline to load files into a data warehouse, we should start with the files we want to important. When we think about those files, it’s likely that we’ll have more than one file to ingest, with new files arriving over time. Because of this, we want to avoid hardcoding the pipeline for a single file.

Instead, we can use a [run configuration](https://docs.dagster.io/guides/operate/configuration/run-configuration) to parameterize the process. This allows us to dynamically specify which file to load each time we execute the pipeline.

First, we’ll define a run configuration so we can set the file path. In the `defs/assets.py` file add the code for the run configuration:

```python
import dagster as dg
from pathlib import Path

class IngestionFileConfig(dg.Config):
    path: str
```

Run configurations inherit from the Dagster `Config` class and allow us to define schemas that can be used in our Dagster assets.

Next, we will write an asset that uses this config. To make things easier, the asset will be designed to look within a specific directory relative to the asset file itself. This way, we only need to provide the file name, rather than the full path, when specifying the configuration:

```python
@dg.asset()
def import_file(context: dg.AssetExecutionContext, config: IngestionFileConfig) -> str:
    file_path = (
        Path(__file__).absolute().parent / f"../../../data/source/{config.path}"
    )
    return str(file_path.resolve())
```

This asset will take in the run config and return the full file path string of a file in the `dagster_and_etl/data/source` directory.

## Loading data

Now that we’ve identified the file we want to load, we can define the destination. In this case, we’ll use [DuckDB](https://duckdb.org/). DuckDB is an in-process Online Analytical Processing (OLAP) database similar to Redshift and Snowflake, but designed to run locally with minimal setup.

In order to use DuckDB we need to establish a connection with our database. In Dagster we can do this with resources, so in the `resources.py` file, add the following:

```python
import dagster as dg
from dagster_duckdb import DuckDBResource

@dg.definitions
def resources():
    return dg.Definitions(
        resources={
            "database": DuckDBResource(
                database="data/staging/data.duckdb",
            ),
        }
    )
```

The code above does the following:
1. Maps the `DuckDBResource` resource to the `Definitions` object.
2. Initializes the `DuckDBResource` to use the local file at `data/staging/data.duckdb` as the backend.

Defining our resource here means we can use it throughout out Dagster project.

## DuckDB asset

Like most databases, DuckDB offers multiple ways to ingest data. One common way when working with files is using DuckDB’s [`COPY`](https://duckdb.org/docs/stable/sql/statements/copy.html) statement. A typical COPY command follows this pattern:

```sql
COPY {table name} FROM {source}
```

This can include additional parameters to specify things like file type and formatting, but DuckDB often infers these settings correctly so we will not worry about it here.

As well as loading data into DuckDB, we need a destination table defined. We can design an asset that creates a table to match the schema of our file and load the file:

```python
from dagster_duckdb import DuckDBResource

@dg.asset(
    kinds={"duckdb"},
)
def duckdb_table(
    context: dg.AssetExecutionContext,
    database: DuckDBResource,
    import_file,
):
    table_name = "raw_data"
    with database.get_connection() as conn:
        table_query = f"""
            create table if not exists {table_name} (
                date date,
                share_price float,
                amount float,
                spend float,
                shift float,
                spread float
            ) 
        """
        conn.execute(table_query)
        conn.execute(f"copy {table_name} from '{import_file}';")
```

The code above does the following:

1. Connects to DuckDB using the Dagster resource `DuckDBResource`.
2. Uses the DuckDB connection to create a table `raw_data` if that tables does not already exist. We define the schema of the table ourselves, knowing the structure of the data.
3. Runs a `COPY` for file path from the `import_file` asset into the `raw_data` table. `COPY` is an append command so if we run the command twice, the data will be loaded again.

## Executing the assets

These two assets are all we need to ingest the data and there are multiple ways to do so in Dagster.

### Command line (`dg launch`)

```bash
dg launch --assets import_file,duckdb_table --config-json "{\"resources\": {\"database\": {\"config\": {\"database\": \"data/staging/data.duckdb\"}}}, \"ops\": {\"import_file\": {\"config\": {\"path\": \"2018-01-22.csv\"}}}}"
```
### Web UI (`dg dev`)

```bash
dg dev
```

Within the UI, materialize the assets while providing the following run execution:

```yaml
resources:
  database:
    config:
      database: data/staging/data.duckdb
ops:
  import_file:
    config:
      path: 2018-01-22.csv
```

![File import DAG](/images/dagster-etl/lesson-3/file-import-dag.png)

In either case (whether using the CLI or the UI) remember that we need to provide a value for the file path as a run configuration in orders to execute the assets.

## Confirm data

To check that everything has loaded correctly, we can connect to the DuckDB database using the [DuckDB CLI](https://duckdb.org/docs/stable/clients/cli/overview.html) and run a query for the table we just made.

```bash
> duckdb data/staging/data.duckdb
D SELECT * FROM raw_data;
┌────────────┬─────────────┬────────────┬────────┬──────────┬──────────┐
│    date    │ share_price │   amount   │ spend  │  shift   │  spread  │
│    date    │    float    │   float    │ float  │  float   │  float   │
├────────────┼─────────────┼────────────┼────────┼──────────┼──────────┤
│ 2018-09-28 │      264.77 │ 33597288.0 │ 270.26 │    278.0 │  260.555 │
│ 2018-09-27 │      307.52 │  7337760.0 │  312.9 │   314.96 │   306.91 │
│ 2018-09-26 │      309.58 │  7835863.0 │ 301.91 │   313.89 │ 301.1093 │
│ 2018-09-25 │      300.99 │  4472287.0 │  300.0 │    304.6 │    296.5 │
│ 2018-09-24 │      299.68 │  4834384.0 │ 298.48 │ 302.9993 │   293.58 │
│ 2018-09-21 │       299.1 │  5038497.0 │  297.7 │   300.58 │   295.37 │
│ 2018-09-20 │      298.33 │  7332477.0 │ 303.56 │   305.98 │   293.33 │
│ 2018-09-19 │      299.02 │  8264353.0 │ 280.51 │    300.0 │    280.5 │
└────────────┴─────────────┴────────────┴────────┴──────────┴──────────┘
```
