---
title: "Lesson 2: Create a new project (without the skill)"
module: 'ai_driven_data_engineering'
lesson: '2'
---

# Create a new project (without the skill)

First we’ll create a Dagster project without using any additional skills or context. This gives you a baseline: what a capable agent does when it has no Dagster-specific guidance.

## Scaffold the project

Use a generic prompt such as:

```text
create a new Dagster project called university
```

![Without 1](/images/ai-driven-data-engineering/lesson-2/without-1.png)

The agent will look up how to create a Dagster project and might run something like:

```bash
dagster project scaffold --name university
```

That uses the older `dagster project scaffold` CLI, which produces a flat layout (e.g. `university/university/` with `__init__.py`, `assets.py`, `definitions.py`).

## Generate assets

Next, ask the agent to add assets that load data into DuckDB from external CSV URLs:

```text
create 3 assets in the university Dagster project that load data into DuckDB tables for the following external files:

https://raw.githubusercontent.com/dbt-labs/jaffle-shop-classic/refs/heads/main/seeds/raw_customers.csv
https://raw.githubusercontent.com/dbt-labs/jaffle-shop-classic/refs/heads/main/seeds/raw_orders.csv
https://raw.githubusercontent.com/dbt-labs/jaffle-shop-classic/refs/heads/main/seeds/raw_payments.csv
```

The agent will add code (often in `assets.py` or similar) and may or may not use `dagster-duckdb` or correct project layout. You get a working pipeline, but structure and tooling are whatever the model infers.

## What you get

After scaffolding and adding assets, the project might look like:

```text
tree university/university

university/university
├── __init__.py
├── assets.py
└── definitions.py
```

When relying on a coding agent without providing it with additional skills or specific context, the agent often resorts to general patterns it has seen before, rather than the best or most idiomatic practices for a given tool. This limitation isn't unique to Dagster—agents tend to produce better, more robust solutions when given guidance tailored to the technology or task at hand. Without those extra hints, the agent’s work is functional, but usually not as deep, maintainable, or aligned with expert usage.

![Project layout without the skill](/images/ai-driven-data-engineering/lesson-2/project-without-skills.png)
