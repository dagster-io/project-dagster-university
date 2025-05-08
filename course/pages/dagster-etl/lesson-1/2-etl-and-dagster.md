---
title: "Lesson 1: ETL and Dagster"
module: 'dagster_etl'
lesson: '1'
---

# ETL and Dagster

One of Dagster’s core strengths is providing full lineage visibility. This often starts by consolidating disparate datasets. Think about your own data stack. You likely have many different systems collecting and storing data that you want to use. Managing this complexity at scale becomes overwhelming without a dedicated system in place to account for the work being done across your pipelines.

When visualizing your data stack, it’s often helpful to think of data flowing from left to right. On the far left, you typically find your raw data sources and the ETL processes that bring that data into your platform. This is a logical starting point for building out a data platform: focusing on ETL assets helps you concentrate on the most important datasets and avoid duplicating effort.

![ETL assets 1](/images/dagster-etl/lesson-1/etl-assets-1.png)

Dagster is particularly well-suited for managing ETL pipelines because source assets are often reused across multiple downstream projects. For example, if you're ingesting data from an application database, that data may feed into both analytics dashboards and machine learning workflows. This is where Dagster’s asset-based perspective shines by helping you reason about data dependencies and usage across your organization.

![ETL as assets 2](/images/dagster-etl/lesson-1/etl-assets-2.png)

## ETL and Dagster assets

Consider a pipeline that ingests data from your application database, you're likely pulling in multiple tables or objects, each destined for a specific schema and table in your data warehouse.

![ETL as assets 1](/images/dagster-etl/lesson-1/etl-as-assets-1.png)

Each of these entities should be tracked as its own asset, so you can associate downstream processes with each one individually. That granularity gives you the ability to monitor, reason about, and recover from failures more effectively.

For example, if one source table fails to ingest, Dagster allows you to quickly understand which downstream assets and applications are impacted. This level of observability and control is what makes asset-based orchestration so powerful — especially in the context of managing critical ETL pipelines.

![ETL as assets 2](/images/dagster-etl/lesson-1/etl-as-assets-2.png)
