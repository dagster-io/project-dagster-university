---
title: "Lesson 5: Agents and Components"
module: 'ai_driven_data_engineering'
lesson: '5'
---

# Agents and Components

Dagster is an orchestrator: it’s meant to span many services and tools. Integrations are a core part of that story. At the same time, the more flexibility you give an agent, the more room there is for inconsistent structure and one-off code. Components are how we keep integrations predictable and agent-friendly.

## Integrations as a core part of Dagster

Dagster doesn’t replace your data tools. It orchestrates them. You typically connect:

- **Transformations**: e.g. dbt, Pandas, SQL
- **Storage and movement**: e.g. S3, DuckDB, data lakes, replication tools like Sling
- **Quality and validation**: e.g. Great Expectations, dbt tests

So integrations (the libraries and patterns that map these tools into Dagster) are central. The [Dagster Integrations](https://docs.dagster.io/integrations) ecosystem covers 82+ integrations; the `dagster-expert` skill gives the agent the right context to pick, configure, and use them.

## What are Components?

[Components](https://docs.dagster.io/guides/build/components) are predefined layouts for common integrations. They let you map other services (e.g. a dbt project, a Sling replication job) into Dagster in a consistent way: standard file locations, standard config shapes, and standard Dagster objects (assets, resources, jobs).

A good use case for Components would be [dbt](https://www.getdbt.com/). dbt  is one of the most common integrations for Dagster so we try and make it as easy as possible with a dedicated dbt Component ([`DbtProjectComponent`](https://docs.dagster.io/integrations/libraries/dbt)). The user simply points Dagster at their dbt project and profiles, and the Component turns dbt models (and optionally tests) into Dagster assets with the right dependencies and metadata.

This is very helpful but does require some understanding of the component, or a skill that provides that understanding.

## Why Components work well with agents

Like `dg`, Components reduce the surface area the agent interacts with when generating code. Instead of the agent inferring:

- Where to put dbt config
- How to wire dbt models to Dagster assets
- How to add replication (e.g. DuckDB → S3) and where that config lives

The agent can scaffold a Component with `dg` and then fill in the integration-specific bits (dbt models, Sling YAML, etc.). That means:

- **Less ambiguity**: the layout and patterns are fixed; the agent follows them.
- **Best practices by default**: components encode how we recommend using each integration with Dagster.
- **Easier iteration**: you can alternate between `dg` / `dbt` / Sling commands and let the agent suggest the next step, with a clear notion of “what good looks like.”

![Prompt with the component](/images/ai-driven-data-engineering/lesson-5/prompt-component.png)
