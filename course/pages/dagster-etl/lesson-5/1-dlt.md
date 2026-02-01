---
title: "Lesson 5: dlt"
module: 'dagster_etl'
lesson: '5'
---

# dlt

One ETL framework we're particularly excited about is [data load tool (dlt)](https://dlthub.com/docs/intro). dlt is an open-source, lightweight Python library designed to simplify data loading. It takes care of many of the more tedious aspects of ETL, including schema management, data type handling, and normalization, so you can focus on what matters most.

dlt supports a wide range of popular sources and destinations, which means you can move data between systems without having to build and maintain all the supporting infrastructure yourself. While it still gives you the flexibility to handle custom or complex data workflows, it eliminates much of the boilerplate code you'd otherwise need to write, making your pipelines cleaner, more maintainable, and faster to develop.

![dlt](/images/dagster-etl/lesson-5/dlt.png)

## Key dlt Features

Before we dive into examples, let's understand some of dlt's most powerful features:

### Write Dispositions

dlt supports three write dispositions that control how data is loaded into your destination:

- **`replace`**: Completely replaces the destination table with new data on each load. Useful for dimension tables or when you always want fresh data.
- **`append`**: Adds new records to existing data. Ideal for event logs or fact tables where you're continuously adding new records.
- **`merge`**: Performs an upsert operation, updating existing records and inserting new ones based on a primary key. Supports Slowly Changing Dimension Type 2 (SCD2) for tracking historical changes.

### Incremental Loading

For large datasets, loading everything on each run is inefficient. dlt provides built-in incremental loading that tracks which data has already been processed:

- **Cursor-based loading**: Track a timestamp or ID column to only load new or updated records
- **State management**: dlt automatically stores state in a `_dlt_pipeline_state` table, so you can resume from where you left off

### Schema Evolution

dlt handles schema changes automatically. If your source data adds new columns, dlt will update the destination schema accordingly—no manual migrations required.

### Verified Sources

While we'll build custom sources in this course to learn the fundamentals, dlt provides [verified sources](https://dlthub.com/docs/dlt-ecosystem/verified-sources/)—pre-built, tested connectors for popular data sources like:

- **SQL databases**: PostgreSQL, MySQL, SQL Server, etc.
- **APIs**: Stripe, GitHub, Slack, Zendesk, HubSpot, and more
- **Cloud storage**: S3, Google Cloud Storage, Azure Blob
- **SaaS platforms**: Salesforce, Notion, Airtable

These verified sources handle authentication, pagination, rate limiting, and error handling out of the box. For production use cases, always check if a verified source exists before building your own.

### REST API Source

For APIs without a verified source, dlt provides a generic [REST API source](https://dlthub.com/docs/dlt-ecosystem/verified-sources/rest_api) that can connect to any REST API with minimal configuration:

```python
from dlt.sources.rest_api import rest_api_source

source = rest_api_source({
    "client": {"base_url": "https://api.example.com"},
    "resources": [
        {
            "name": "users",
            "endpoint": {"path": "users"},
        }
    ]
})
```

This approach is more declarative than writing custom extraction code and handles common patterns like pagination automatically.

Let's look at a simple dlt example.
