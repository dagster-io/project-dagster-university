---
title: "Lesson 3: Overview"
module: 'dagster_etl'
lesson: '3'
---

# Overview

We'll begin by loading data from an external system into a data warehouse. In production, this source might be something like S3 or Azure Blob Storage, but for now, we’ll keep things simple by using the local filesystem.

This is one of the most common ETL use cases, and many data warehouses support it natively. For example, loading data from S3 can often be accomplished by executing a SQL command directly within the warehouse. However, there are also situations where some level of custom processing is needed before the data can be ingested.

In either case, this provides a solid starting point to explore the different ways ETL can be implemented in Dagster.

![API ETL](/images/dagster-etl/lesson-3/csv-etl.png)
