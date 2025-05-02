---
title: "Lesson 3: Overview"
module: 'dagster_etl'
lesson: '3'
---

We are going start with a simple example, loading data from external cloud storage system (like S3 or Azure Blob Storage) and load that data into database.

This is such a common use case, many systems support this natively. If you needed to load data from S3 into most data warehouses, this can be accomplished by running a SQL statement within the data warehouse itself. However there are also cases where you need to do some amount of custom processing to the data before it can be loaded.

Either way, this will serve as a good first use case as we describe the various ways to perform ETL with Dagster.