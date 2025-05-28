---
title: "Lesson 3: Cloud storage"
module: 'dagster_etl'
lesson: '3'
---

# Cloud storage

What if you want to change the source of your ETL pipeline from local files to cloud storage? In most real-world scenarios, data is not stored locally but in a managed storage layer like Amazon S3. Let’s walk through how to modify your Dagster assets to support S3 as the source for the ingestion pipeline.

**Note:** We won’t run this code since we’re not setting up an actual S3 bucket for testing. Instead, we’ll focus on the structure and design changes required to support this integration.

## Redefining the run configuration

If you’re new to AWS Simple Storage Service (S3):
S3 is a cloud-based object storage service that lets you upload and retrieve data using "buckets" and "paths" (which are really just key prefixes).

```bash
s3://<bucket-name>/<optional-folder-path>/<object-name>
```

To support dynamic S3-based ingestion, we'll define a new config schema called IngestionFileS3Config. This configuration will have two fields:

| Property | Type | Description |
| --- | --- |  --- |
| `bucket` | string | The name of the S3 bucket |
| `path` | string | The path within the S3 bucket of the object |

What would this run configuration `IngestionFileS3Config` looke like:

```python {% obfuscated="true" %}
class IngestionFileS3Config(dg.Config):
    bucket: str
    path: str
```

This could be modeled as a single string (e.g. full S3 URI), but splitting bucket and path is often more practical, especially if your pipelines reuse the same bucket across different datasets.

## S3 assets

Next, let’s update the import_file and duckdb_table assets to support S3-based ingestion. One key thing to note about DuckDB is that it can load data directly from S3 using a COPY statement, like so:

```sql
COPY my_table FROM 's3://my-bucket/my-file.csv' (FORMAT CSV, HEADER);
```

However, this approach only works if the S3 bucket is public. Most real-world buckets are private, but for the purpose of this example, we’ll assume the S3 bucket is publicly accessible and does not require authentication.

With this background we can update our asset code:

```python {% obfuscated="true" %}
@dg.asset(
    kinds={"s3"},
)
def import_file_s3(
    context: dg.AssetExecutionContext,
    config: IngestionFileS3Config,
) -> str:
    s3_path = f"s3://{config.bucket}/{config.path}"
    return s3_path


@dg.asset(
    kinds={"duckdb"},
)
def duckdb_table_s3(
    context: dg.AssetExecutionContext,
    database: DuckDBResource,
    import_file_s3: str,
):
    table_name = "raw_s3_data"
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
        conn.execute(f"copy {table_name} from '{import_file_s3}' (format csv, header);")
```

Not much needs to change when moving from local files to cloud storage. The main takeaway is that loading static files from S3 closely mirrors loading them from the local filesystem. All the patterns and tools we've already applied (partitions, schedules, sensors) still apply. Whether the file is local or in S3 bucket, the logic for defining and orchestrating data assets remains largely the same.
