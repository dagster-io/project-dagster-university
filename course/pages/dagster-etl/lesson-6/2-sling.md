---
title: "Lesson 6: Sling"
module: 'dagster_etl'
lesson: '6'
---

# Sling

While we can use dlt for database replication, in this lesson we’ll introduce another open-source ETL framework: [Sling](https://docs.slingdata.io/). Sling is a modern tool designed to simplify both real-time and batch data replication. It helps teams move data from databases like Postgres and MySQL into cloud data warehouses such as Snowflake or Redshift with minimal setup. Exposing all configuration through a simple YAML interface. 

Sling differs from dlt in that it is declarative by design. While dlt offers greater flexibility and can handle data ingestion from a wide variety of sources (such as our custom NASA API), Sling is purpose-built for database replication and excels at managing the complexities of moving data and schema evolution.
