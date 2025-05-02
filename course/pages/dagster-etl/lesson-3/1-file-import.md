---
title: "Lesson 3: File import"
module: 'dagster_etl'
lesson: '3'
---

# File import

As mentioned we will start by loading a file into a data warehouse. Most of the principles covered here will apply regardless of the source and destination. We can pull data from cloud storage and load them into a cloud data warehouse. But to keep things simple to start we will load a local file from a directory into DuckDB warehouse also running locally.

## Config

Let's think about the first asset we need. If we are building a pipeline to load files into the data warehouse, we likely have more than one file to bring in and more files over time. Therefore we don't want to build a pipeline that is hardcoded for a single file.

Instead we can use a [run configuration](https://docs.dagster.io/guides/operate/configuration/run-configuration) to parameterize our process so that multiple files can be loaded.

First we need a run configuration so we can set the file path:

```python
class FilePath(dg.Config):
    path: str
```

Next we can use that run configuration within an asset. In order to make things easier, we the asset will ensure we are looking within a specific directory relative to the asset file so we can simplify the file name we need to provide:

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

Now we can set the file path at runtime to look at any file within the `data/source` directory.

## Loading data

Now that we the file we want to load from our source, we can define the destination. In this case we will use [DuckDB](https://duckdb.org/) which is an Online Analytical Processing (OLAP) database similar to Redshift and Snowflake that can be run locally.

DuckDB is a very useful tool for working with large datasets and can actually read directly from files. But to demonstrate the ETL process, we will load all the data from our file into the DuckDB database.

One way to do this is a with a [`COPY`](https://duckdb.org/docs/stable/sql/statements/copy.html) statement within DuckDB. This is DuckDB's primary way to load external data. A `COPY` statement generally follows this a general pattern:

`COPY {table name} FROM {source}`

There are other parameters we can include for things like file type and formatting but DuckDB is pretty good about assuming the correct configuration.

With that, we are ready to create our second asset.

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
2. Uses the DuckDB connection to create a table `raw_data` if it does not already exist in the DuckDB database.
3. Copies the data from the file returned by the `import_file` asset into the `raw_data` table.

Now we can execute these assets using `dg`

```bash
dg launch --assets import_file,duckdb_table --config-json
```

## Confirm data

Then to confirm everything has loaded we can connect to our DuckDB database and query the table.

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
