---
title: "Lesson 1: ETL and Dagster"
module: 'dagster_etl'
lesson: '1'
---

# ETL and Dagster

One of Dagster’s strengths is giving you full lineage of all the data assets within your organization. Usually this starts by consolidating disparate data sets. Think about your own data stack. You likely have many different systems collection and storing data that you want to use. Trying to manage this at scale becomes too much of a burden without a dedicated system in place to account for all the work that is occurring.

When envisioning your data stack it usually makes sense to view the flow of data from left to right. In most cases raw sources and their ETL processes are the furthest to the left in those diagrams.

![ETL assets 1](/images/dagster-etl/lesson-1/etl-assets-1.png)

This makes sense and is a great starting point for building out your data platform. Focusing on these ETL assets first will help you focus on the data sets that are most important to you and ensure you do not duplicate work.

Another reason Dagster is particularly well suited for managing your ETL assets is because these source assets tend to be used multiple times. If you are bringing in data from your application database, that may feed into multiple different analytics and machine learning projects. This is where having an asset based perspective can be useful.

![ETL as assets 2](/images/dagster-etl/lesson-1/etl-assets-2.png)

## ETL and Dagster assets

We already mentioned that ETL tasks lend themselves to assets. When you deconstruct  the structure of an ETL process, this makes sense. Keeping with our example of ingestion our application database. Most likely we want to ingest multiple objects into our destination.

These can be multiple schemas and tables, each of which will sync to a specific schema and table in our destination system. We want to track to each of these objects individually and be able to associate downstream processes with each of these on their own.

![ETL as assets 1](/images/dagster-etl/lesson-1/etl-as-assets-1.png)

Likewise we want to be able to assess of all of these objects individually. If one of our tables fails, we want to be able to quickly understand the full lineage of which of our data applications are impacted.

![ETL as assets 2](/images/dagster-etl/lesson-1/etl-as-assets-2.png)
