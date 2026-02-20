---
title: "Lesson 4: Create a new project (with the skill)"
module: 'ai_driven_data_engineering'
lesson: '4'
---

# Create a new project (with the skill)

Now we’ll do the same thing using the **Dagster Expert** skill. Same goal—scaffold a project and add three assets that load CSVs into DuckDB—but with skill-driven behavior and `dg` at the center.

---

## Scaffold the project with the skill

Use the skill-prefixed prompt:

```bash
> dagster-expert create a new Dagster project called university
```

![Prompt with the Dagster Expert skill](/images/ai-driven-data-engineering/lesson-4/prompt-agent-dg-skill.png)

With the skill, the agent uses the **latest recommended** project creation command, for example:

```bash
uvx create-dagster project university --uv-sync
```

So you get a modern layout (e.g. `src/university/`, `pyproject.toml`, `uv`) instead of the older `dagster project scaffold` flat layout. At first glance the result may look similar to “a new project,” but the structure and tooling are the ones Dagster recommends today.

---

## Add the three assets with the skill

Ask for the same three assets, again with the skill:

```bash
> dagster-expert create 3 assets in the university Dagster project that load data into DuckDB tables for the following external files:

https://raw.githubusercontent.com/dbt-labs/jaffle-shop-classic/refs/heads/main/seeds/raw_customers.csv
https://raw.githubusercontent.com/dbt-labs/jaffle-shop-classic/refs/heads/main/seeds/raw_orders.csv
https://raw.githubusercontent.com/dbt-labs/jaffle-shop-classic/refs/heads/main/seeds/raw_payments.csv
```

Here the benefit of **AI + CLI** shows up clearly.

---

## How the skill and `dg` work together

The skill steers the agent toward `dg` and an opinionated project layout. Dagster works with any package manager, but the skill and this course assume `uv` for dependency management.

1. **Dependencies** — The agent sees that DuckDB is needed and adds it via the project’s package manager, e.g.:

   ```bash
   uv add dagster-duckdb
   ```

2. **Scaffolding in the right place** — Instead of inventing file locations, the agent uses `dg` so files land where the project expects:

   ```bash
   dg scaffold defs dagster.asset assets/raw_data.py
   ```

   That keeps definitions in the right place and reduces the context the agent needs to guess.

3. **Validation** — After editing, the agent can confirm that definitions load and are valid (without running business logic):

   ```bash
   dg check defs
   ```

   These quick checks make it easier to do larger changes in small, verifiable steps.

4. **Next steps** — When checks pass, the skill often suggests the logical next action. For new assets, that might be running them:

   ```bash
   dg launch --assets "raw_customers,raw_orders,raw_payments"
   ```

---

## Resulting layout

After scaffolding and adding the three assets with the skill, the project might look like:

```bash
tree university/src/university
├── __init__.py
├── definitions.py
└── defs
    ├── __init__.py
    ├── assets
    │   └── raw_data.py
    └── resources.py
```

![Project layout with the skill](/images/ai-driven-data-engineering/lesson-4/project-with-skills.png)

So you get a defs-based layout: assets under `defs/assets/`, shared resources in `defs/resources.py`, and a single `definitions.py` that wires everything together. This matches how `dg` and the Dagster Expert skill expect a project to be structured and makes it easier to add more assets, jobs, and schedules later.
