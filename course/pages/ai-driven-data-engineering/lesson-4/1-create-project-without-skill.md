---
title: "Lesson 4: Create a new project (without the skill)"
module: 'ai_driven_data_engineering'
lesson: '4'
---

# Create a new project (without the skill)

First we’ll create a Dagster project **without** using the Dagster Expert skill. This gives you a baseline: what a capable agent does when it has no Dagster-specific guidance.

---

## Scaffold the project

Use a generic prompt such as:

```bash
/create a new Dagster project called university
```

![Generic prompt to the agent](/images/ai-driven-data-engineering/lesson-4/prompt-agent.png)

The agent will look up how to create a Dagster project and typically run something like:

```bash
dagster project scaffold --name university
```

That uses the older `dagster project scaffold` CLI, which produces a flat layout (e.g. `university/university/` with `__init__.py`, `assets.py`, `definitions.py`). No `dg` or Components-style layout is implied.

---

## Generate assets

Next, ask the agent to add assets that load data into DuckDB from external CSV URLs:

```bash
/create 3 assets in the university Dagster project that load data into DuckDB tables for the following external files:

https://raw.githubusercontent.com/dbt-labs/jaffle-shop-classic/refs/heads/main/seeds/raw_customers.csv
https://raw.githubusercontent.com/dbt-labs/jaffle-shop-classic/refs/heads/main/seeds/raw_orders.csv
https://raw.githubusercontent.com/dbt-labs/jaffle-shop-classic/refs/heads/main/seeds/raw_payments.csv
```

The agent will add code (often in `assets.py` or similar) and may or may not use `dagster-duckdb`, correct project layout, or `dg` for validation. You get a working pipeline, but structure and tooling are whatever the model infers.

---

## What you get

After scaffolding and adding assets, the project might look like:

```bash
tree university/university

university/university
├── __init__.py
├── assets.py
└── definitions.py
```

![Project layout without the skill](/images/ai-driven-data-engineering/lesson-4/project-without-skills.png)

So you end up with a **flat, minimal layout**: a single `assets.py` and a single `definitions.py`. It works, but there’s no standard `defs/` structure, no `dg`-driven scaffolding, and no built-in habit of running `dg check defs` to validate. In the next sections we’ll redo the same workflow **with** the Dagster Expert skill and compare.
