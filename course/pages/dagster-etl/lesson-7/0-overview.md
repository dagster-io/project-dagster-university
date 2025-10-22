---
title: "Lesson 7: Overview"
module: 'dagster_etl'
lesson: '7'
---

# Overview

We’ve now covered a wide range of ETL use cases, from static files and APIs to database replication. Interestingly, as our pipelines have grown more complex, our code has actually become simpler. That’s thanks to the thoughtful abstractions provided by tools like dlt, Sling and Dagster.

The last topic we’ll cover is [Dagster Components](https://docs.dagster.io/guides/build/components/). So far, we’ve seen how Dagster can work with frameworks like dlt and Sling to build robust pipelines. However, coordinating across frameworks can be difficult. You have to initialize configurations with different CLIs, manage configurations and know how everything connects.

In order to simplify this development process, Dagster unifies this all within components. Their goal is to make developing these types of integrations much easy and reduce the amount of code users are responsible for maintaining.

In this section we will redefine the Sling integration from the previous lesson with components.