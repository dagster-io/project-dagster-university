---
title: "Lesson 4: Overview"
module: 'dagster_etl'
lesson: '4'
---

# Overview

Now that we’ve covered CSV-based ingestion, let’s move on to another common pattern: loading data from an API. We’ll continue using the same destination (DuckDB) but introduce some new Dagster functionality to fetch data from an external API, apply light processing, and load the results into the database. This pattern is useful when working with third-party services, public datasets, or internal APIs that expose structured data for integration.

![API ETL](/images/dagster-etl/lesson-4/api-etl.png)
