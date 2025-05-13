---
title: "Lesson 3: File import"
module: 'dagster_etl'
lesson: '3'
---

# File import

As mentioned, we’ll start by loading a file into a data warehouse. While we’re using a local file and a local DuckDB instance for simplicity, the same principles apply regardless of the source and destination. You could easily adapt this pipeline to pull data from cloud storage and load it into a cloud-based data warehouse.

## Config

Let’s consider the first asset we need. If we’re building a pipeline to load files into a data warehouse, it’s likely that we’ll have more than one file to ingest, with new files arriving over time. Because of this, we want to avoid hardcoding the pipeline for a single file.

Instead, we can use a [run configuration](https://docs.dagster.io/guides/operate/configuration/run-configuration) to parameterize the process. This allows us to dynamically specify which file to load each time we execute the pipeline.

First, we’ll define a run configuration to set the file path:

```python
class FilePath(dg.Config):
    path: str
```

Run configurations inherit from the Dagster `Config` class and allow us to define schemas that can be used in our Dagster assets.

Next, we will write an asset that uses that config. To make things easier, the asset will be designed to look within a specific directory relative to the asset file itself. This way, we only need to provide the file name, rather than the full path, when specifying the configuration:

```python
@dg.asset(
    group_name="static_etl",
)
def import_file(context: dg.AssetExecutionContext, config: FilePath) -> str:
    file_path = (
        Path(__file__).absolute().parent / f"../../../../data/source/{config.path}"
    )
    return str(file_path.resolve())
```

This asset will take in the run config and return the full file path string of a file in the `data/source` directory.

## Loading data

Now that we’ve identified the file we want to load, we can define the destination. In this case, we’ll use [DuckDB](https://duckdb.org/). DuckDB is an in-process Online Analytical Processing (OLAP) database similar to Redshift and Snowflake, but designed to run locally with minimal setup.

DuckDB is a powerful tool for working with large datasets and can even read directly from files without needing to import them. However, to demonstrate a more traditional ETL workflow, we’ll load the data from our file directly into a DuckDB table.

Like most databases, DuckDB offers multiple ways to ingest data. One common way when working with files is using DuckDB’s [`COPY`](https://duckdb.org/docs/stable/sql/statements/copy.html) statement. A typical COPY command follows this pattern:

```sql
COPY {table name} FROM {source}
```

This can include additional parameters to specify things like file type and formatting, but DuckDB often infers these settings correctly so we will not worry about it here.

But before we load the data into DuckDB, we need a destination table. We can design an asset that creates a table to match the schema of our file and load the file:

```python
@dg.asset(
    kinds={"duckdb"},
    group_name="static_etl",
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
        conn.execute(f"COPY {table_name} FROM '{import_file}';")
```

The code above does the following:

1. Connects to DuckDB using the Dagster resource `DuckDBResource`.
2. Uses the DuckDB connection to create a table `raw_data` if that tables does not already exist.
3. Runs a `COPY` for file path from the `import_file` asset into the `raw_data` table.

These two assets are all we need to ingest the data. We can execute these assets from the command line using `dg`:

```bash
dg launch --assets import_file,duckdb_table --config-json "{\"config\":{\"ops\":{\"import_file\":\"2018-01-22.csv\"}}}"
```

Remember that since we are using a run configuration, we need to supply a value for the file path in order to execute the assets.

## Confirm data

To check that everything has loaded correctly, we can connect to the DuckDB database using the DuckDB CLI and run a query for the table we just made.

```bash
> duckdb data/staging/duckdb
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
