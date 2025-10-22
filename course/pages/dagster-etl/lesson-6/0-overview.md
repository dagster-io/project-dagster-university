---
title: "Lesson 6: Overview"
module: 'dagster_etl'
lesson: '6'
---

# Overview

We’ve explored several ways to ingest data from external sources, but one approach we haven’t covered yet is moving data between databases. This is a broad category, as databases vary widely in type and behavior. However, the most common scenario and one that many people associate with traditional ETL, is replicating data from an OLTP database (like Postgres or MySQL) into a data warehouse (such as Snowflake or Redshift).

Although this flow is extremely common, and something nearly every data-driven organization performs to some extent, it's also a nuanced and potentially error-prone process. From schema drift and type mismatches to performance bottlenecks and data consistency challenges, moving data between systems requires careful handling and thoughtful architecture.
