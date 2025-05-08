---
title: "Lesson 4: Overview"
module: 'dagster_etl'
lesson: '4'
---

Now that we’ve covered ingestion with CSVs, let’s move on to another common ingestion pattern. Loading data from an API. We’ll continue using the same destination (DuckDB) but introduce some new Dagster functionality to fetch data from an external API and perform light processing before loading it into the database.

![API ETL](/images/dagster-etl/lesson-4/api-etl.png)
