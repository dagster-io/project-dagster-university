---
title: "Lesson 6: Overview"
module: 'dagster_etl'
lesson: '6'
---

We have talked about a lot of different ways to ingest data from external sources. One way we haven't discussed yet is moving data between databases. Moving data between databases is a board term since there are so many different types of databases. But the most common situation that most people think of when they are doing ETL is moving from an OLTP database (Postgres or MySQL) to a data warehouse (Snowflake or Redshift).

Despite it being a very common flow that almost all organizations do to some point. It is a very nuanced operation and one with many potential pitfalls.