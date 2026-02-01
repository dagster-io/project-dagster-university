---
title: "Lesson 6: Sling"
module: 'dagster_etl'
lesson: '6'
---

# Sling

In the previous lesson we used dlt. dlt is great for flexibility but since we know we are doing replication between two systems, we can try something else (though dlt can also do replication).

For this lesson we'll introduce another open-source ETL framework: [Sling](https://docs.slingdata.io/). Sling is a modern tool designed to simplify both real-time and batch data replication. It helps teams move data from databases like Postgres and MySQL into cloud data warehouses such as Snowflake or Redshift with minimal setup. Exposing all configuration through a simple YAML interface. 

Sling differs from dlt in that it is declarative by design. While dlt offers greater flexibility and can handle data ingestion from a wide variety of sources (such as our custom NASA API), Sling is purpose-built for database replication and excels at managing the complexities of moving data and schema evolution.

## Key Sling Features

### Replication Modes

Sling supports several replication modes to handle different data loading scenarios:

- **`full-refresh`**: Drops and recreates the target table with all source data. Simple but can be slow for large tables.
- **`incremental`**: Only loads new or updated records based on a specified `update_key` column (like a timestamp or auto-incrementing ID).
- **`append`**: Adds all source records to the target without checking for duplicates. Fast but can create duplicates if run multiple times.
- **`truncate`**: Clears the target table before loading, but preserves the table structure.

### State Management

For incremental replication, Sling tracks the last successfully replicated value using a state file. You can configure this with the `SLING_STATE` environment variable pointing to a JSON file:

```bash
export SLING_STATE=/path/to/sling_state.json
```

This state file stores the last value of your `update_key` for each stream, allowing Sling to resume from where it left off.

### Schema Evolution

Like dlt, Sling handles schema changes automatically. If source tables add new columns, Sling will add them to the destination as well.

## When to Use Sling vs dlt

Both tools can handle data replication, but they excel in different scenarios:

| Use Case | Recommended Tool | Why |
|----------|------------------|-----|
| Database-to-database replication | **Sling** | Purpose-built for this, handles connection pooling, optimized bulk transfers |
| Custom API integrations | **dlt** | More flexible, supports custom Python logic |
| Complex transformations during load | **dlt** | Supports inline transformations in Python |
| Simple YAML-based configuration | **Sling** | Declarative config, minimal Python needed |
| Incremental loads with cursor tracking | **Both** | Both support this well |
| SCD2 (slowly changing dimensions) | **dlt** | Built-in merge with SCD2 support |
| Real-time/CDC replication | **Neither** | Consider Debezium or similar CDC tools |

**In general:**
- Choose **Sling** when you're replicating between databases and want minimal code
- Choose **dlt** when you need flexibility, custom APIs, or complex transformations
