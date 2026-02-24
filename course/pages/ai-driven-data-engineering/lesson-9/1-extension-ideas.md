---
title: "Lesson 9: Extension ideas"
module: 'ai_driven_data_engineering'
lesson: '9'
---

# Extension ideas

Here are some directions to take the project. For each one, there's a suggested skill and a prompt you could start with—including examples of how to describe intent without knowing the Dagster term. These are starting points, not prescriptions. Follow the conversation wherever it goes.

---

## Add partitions to the raw assets

Right now the raw assets download the full dataset every time they run. That's fine for small CSVs, but it doesn't scale—and it means you can't backfill specific time ranges without re-running everything.

Partitions let each asset run for a specific slice of data (a day, a month, a quarter) independently. You can then backfill the last year one month at a time, or trigger only the partition that covers new data.

**Skill:** `/dagster-expert`

**If you don't know the term:**
```
/dagster-expert I want my raw assets to process data for one month at a time so I can
backfill the last 12 months without running everything in one big job. How do I do this?
```

**If you know the term:**
```
/dagster-expert Add monthly partitions to the three raw assets and update the schedule
to run the current month's partition daily
```

After adding partitions, open the asset catalog and look at how the partition slice view changes the way the assets are represented. Upstream partitions automatically propagate to downstream assets—your dbt models and Sling export can be made partition-aware too.

---

## Add a sensor to trigger on new data

The pipeline currently runs on a fixed schedule. But what if you want it to trigger automatically when a new file lands in S3, or when a new row appears in an external database?

**Sensors** in Dagster poll an external condition and emit run requests when something changes. You don't need to know this term to ask for it.

**Skill:** `/dagster-expert`

**If you don't know the term:**
```
/dagster-expert Instead of running on a schedule, I want the pipeline to start automatically
whenever a new CSV file appears in an S3 bucket. What's the Dagster way to do this?
```

**If you know the term:**
```
/dagster-expert Replace the daily schedule with a sensor that watches an S3 prefix and
triggers a run when a new file appears
```

---

## Bring in a new data source

The pipeline currently pulls from three static CSV URLs. A natural extension is adding a real integration—a database, an API, or a SaaS tool—as a source.

This is a good place to use `/dagster-integrations` to discover what's available before committing to anything. Start by asking what options exist for your source:

```
/dagster-integrations I want to pull data from Postgres into DuckDB as an additional
raw asset. What's the best way to set this up with Dagster?
```

Or if you're not sure what tools fit:

```
/dagster-integrations I want to add another data source to the pipeline. What are good
open-source options for pulling data from REST APIs with Dagster?
```

The skill will suggest options with a comparison and help you scaffold the right Component once you've chosen.

---

## Add a new destination

Instead of (or in addition to) S3, export the `fct_orders` model somewhere else: a data warehouse like BigQuery or Snowflake, a BI tool's embedded database, or a different file format.

**Skill:** `/dagster-integrations`

```
/dagster-integrations I want to export fct_orders to BigQuery instead of (or in addition to) S3.
What's the recommended way to do this with Dagster?
```

If you're not sure what destination fits your use case, describe the constraint:

```
/dagster-integrations I need to get fct_orders into something a BI tool can query directly.
What are my options with open-source Dagster integrations?
```

---

## Enrich the asset catalog with metadata

The pipeline works, but the asset catalog could tell a richer story. Asset descriptions, owners, tags, and materialization metadata make the catalog useful to people who didn't build the pipeline.

**Skill:** `/dagster-expert`

```
/dagster-expert Add descriptions and owner tags to all three raw assets and the dbt
staging models so the asset catalog is self-documenting
```

You can also add **materialization metadata**—row counts, file sizes, timestamps—so each asset run records what it produced:

```
/dagster-expert Update the raw assets to emit row counts as materialization metadata
after each run
```

---

## Extend the dbt project

The current dbt project has staging models and a single facts table. A natural next step is adding more analytical models—aggregations, slowly changing dimensions, or mart-level tables designed for specific use cases.

**Skill:** `/dagster-integrations`

```
/dagster-integrations Add a dbt model called monthly_revenue that aggregates fct_orders
by month and customer, and expose it as a Dagster asset dependent on fct_orders
```

This is also a good opportunity to add more dbt tests—not just `not_null` but referential integrity checks, accepted values, or custom tests for your business rules.

---

## A note on conversations vs. single prompts

The extensions above are starting points, not one-shot prompts. Most of them will involve a back-and-forth conversation: the agent explains the abstraction, you ask a follow-up, it suggests options, you pick one, it scaffolds. That conversation is the workflow.

Don't try to pack everything into a single prompt. Describe what you want, see what the agent produces, check the asset catalog, and then refine. The skills are designed for iterative use, and the `dg check defs` loop means you can move in small, verified steps without worrying about breaking something that was working.
