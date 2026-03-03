---
title: 'Capstone'
module: 'ai_driven_data_engineering'
lesson: 'capstone'
---

# Capstone

You've built a complete ELT pipeline from scratch: raw data into DuckDB, dbt models transforming it into something useful, a Sling export shipping the results to S3, data quality checks, a daily schedule, and clean Python throughout. All from prompts.

This capstone doesn't introduce new concepts. It's an open invitation to keep going.

The best way to solidify an AI-driven workflow is to use it on something you actually care about, or at least something that makes you think. Below is a set of extension ideas and, more importantly, a way of approaching them when you're not sure what to ask for.

## The workflow is the same

Whatever you choose to build next, the approach doesn't change:

Describe the data product or behavior you want. Think about whether the task is about Dagster itself (reach for `/dagster-expert`) or about an external tool like dbt (reach for the dbt skill). Let the agent figure out the mechanics. Check the result in the asset catalog.

The only new challenge is that some of the things you might want to build have names in Dagster that you don't know yet. That's fine.

## You don't need to know the abstraction to ask for it

One of the most useful things you can do with a skill-equipped agent is describe what you want in plain English, without knowing the right Dagster term. The skill will figure it out.

For example: say you want your raw assets to process data one month at a time so you can backfill a year of history without running everything in a single job. You might not know that Dagster calls this **partitions**. That's not a problem. Just describe it:

```text
/dagster-expert I want each of my raw assets to process data for a specific month, so I can backfill the last 12 months one month at a time. How do I set this up?
```

The agent will explain what partitions are, show you how they apply to your project, and scaffold the changes. By the end of the conversation you'll understand the abstraction because you learned it in the context of your actual pipeline, not from a documentation page in the abstract.

## Extension ideas

Here are some directions to take the project. For each one, there's a suggested skill and a prompt you could start with, including examples of how to describe intent without knowing the Dagster term. These are starting points, not prescriptions. Follow the conversation wherever it goes.

### Add partitions to the raw assets

Right now the raw assets download the full dataset every time they run. That's fine for small CSVs, but it doesn't scale, and it means you can't backfill specific time ranges without re-running everything.

Partitions let each asset run for a specific slice of data (a day, a month, a quarter) independently. You can then backfill the last year one month at a time, or trigger only the partition that covers new data.

**If you don't know the term:**
```text
/dagster-expert I want my raw assets to process data for one month at a time so I can
backfill the last 12 months without running everything in one big job. How do I do this?
```

After adding partitions, open the asset catalog and look at how the partition slice view changes the way the assets are represented. Upstream partitions automatically propagate to downstream assets. Your dbt models and Sling export can be made partition-aware too.

### Add a sensor to trigger on new data

The pipeline currently runs on a fixed schedule. But what if you want it to trigger automatically when a new file lands in S3, or when a new row appears in an external database?

**Sensors** in Dagster poll an external condition and emit run requests when something changes. You don't need to know this term to ask for it.

**If you don't know the term:**
```text
/dagster-expert Instead of running on a schedule, I want the pipeline to start automatically
whenever a new CSV file appears in an S3 bucket. What's the Dagster way to do this?
```

**If you know the term:**
```text
/dagster-expert Replace the daily schedule with a sensor that watches an S3 prefix and
triggers a run when a new file appears.
```

### Bring in a new data source

The pipeline currently pulls from three static CSV URLs. A natural extension is adding a real integration (a database, an API, or a SaaS tool) as a source.

This is a good place to use `/dagster-expert` to discover what's available before committing to anything. Start by asking what options exist for your source:

```text
/dagster-expert I want to pull data from Postgres into DuckDB as an additional
raw asset. What's the best way to set this up with Dagster?
```

Or if you're not sure what tools fit:

```text
/dagster-expert I want to add another data source to the pipeline. What are good
open-source options for pulling data from REST APIs with Dagster?
```

The skill will suggest options with a comparison and help you scaffold the right Component once you've chosen.

### Add a new destination

Instead of (or in addition to) S3, export the `fct_orders` model somewhere else: a data warehouse like BigQuery or Snowflake, a BI tool's embedded database, or a different file format.

```text
/dagster-expert I want to export fct_orders to BigQuery instead of (or in addition to) S3.
What's the recommended way to do this with Dagster?
```

If you're not sure what destination fits your use case, describe the constraint:

```text
/dagster-expert I need to get fct_orders into something a BI tool can query directly.
What are my options with open-source Dagster integrations?
```

### Enrich the asset catalog with metadata

The pipeline works, but the asset catalog could tell a richer story. Asset descriptions, owners, tags, and materialization metadata make the catalog useful to people who didn't build the pipeline.

```text
/dagster-expert Add descriptions and owner tags to all three raw assets and the dbt
staging models so the asset catalog is self-documenting.
```

You can also add **materialization metadata** (row counts, file sizes, timestamps) so each asset run records what it produced:

```text
/dagster-expert Update the raw assets to emit row counts as materialization metadata
after each run.
```

### Extend the dbt project

The current dbt project has staging models and a single facts table. A natural next step is adding more analytical models (aggregations, slowly changing dimensions, or mart-level tables designed for specific use cases).

```text
/dagster-expert Add a dbt model called monthly_revenue that aggregates fct_orders
by month and customer, and expose it as a Dagster asset dependent on fct_orders.
```

This is also a good opportunity to add more dbt tests, not just `not_null` but referential integrity checks, accepted values, or custom tests for your business rules.

### Try test-driven development with the agent

The extension ideas above are all feature-first: define what you want to build, then build it. Test-driven development inverts this: you write a failing test first, then prompt the agent to make it pass. The test is both the specification and the exit condition.

For Dagster, this maps naturally to pytest asset tests and asset checks:

**Step 1: Write the test:**
```python
# tests/test_raw_assets.py
def test_raw_payments_has_rows(duckdb_resource):
    """raw_payments asset should load at least one row from the source CSV."""
    conn = duckdb_resource.get_connection()
    result = conn.execute("SELECT COUNT(*) FROM raw_payments").fetchone()
    assert result[0] > 0
```

**Step 2: Prompt the agent to implement until the test passes:**
```text
/dagster-expert Implement the raw_payments asset so this test passes:

[paste test]

The CSV is at [URL]. Use the _make_raw_asset() factory like the other raw assets.
Verify by running: uv run pytest tests/test_raw_assets.py::test_raw_payments_has_rows -x
```

The test serves as the specification and the validation. The agent has a concrete target: not "does this look reasonable?" but "does this specific assertion pass?". This also composes with the writer/reviewer pattern from Lesson 8: write the test in Session A, implement in Session B.

## Getting help

If you get stuck or have questions, you can:

- Join the [Dagster Slack](https://dagster.io/community) community and ask a question in our `#ask-community` channel
- Find solutions and patterns in our [GitHub discussions](https://github.com/dagster-io/dagster/discussions)
- Check out the [Dagster Docs](https://docs.dagster.io/)

---

## Share your work!

We'd love to see what you create! When you're done, you can:

- Add the project to a public GitHub repository
- Tag us on your socials, like Twitter/X or LinkedIn! We're `@dagster` on both platforms.
- Join the Dagster Slack community and share your work in `#community-showcase`
