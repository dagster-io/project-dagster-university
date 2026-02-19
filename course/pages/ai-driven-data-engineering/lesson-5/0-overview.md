---
title: "Lesson 5: Overview — Integrations, Components, and AI"
module: 'ai_driven_data_engineering'
lesson: '5'
---

# Overview: Integrations, Components, and AI

This lesson focuses on **integrations** and **Components** in Dagster, and why building around AI and Components works so well. You’ll use the **Dagster Integrations** skill to add dbt and Sling, and see how Components keep the agent on a clear, best-practice path.

---

## What we'll cover

- **Overview of the Dagster integration skill** — Why integrations are central to Dagster (as an orchestrator spanning many services and tools) and what the `dagster-integrations` skill provides.

- **Agents and Components** — How Components give predefined layouts for common integrations (e.g. dbt) and, like `dg`, reduce the surface area the agent interacts with. Less ambiguity and code that adheres to Dagster best practices.

- **Adding dbt** — Generate a dbt project from scratch based on the raw assets from Lesson 4, using the `dagster-integrations` skill and the dbt Component. Scaffold with `dg`, alternate between `dg` and `dbt` commands, and use the expert skill to debug if needed.

- **Modifying our project** — Connect dbt assets to raw assets, set asset group names (e.g. `transformation`), and add dbt tests (e.g. NOT NULL on id columns).

- **Additional components** — Use the agent to discover integration options (e.g. “export fct_orders to S3 with open-source tools”), then add another Component (e.g. Sling for DuckDB → S3) and wire dependencies.

- **When to use each skill** — When to reach for `dagster-expert` (core Dagster: assets, checks, automation, `dg`) vs `dagster-integrations` (connecting to external tools). Add an asset check with the expert skill, then refine it to use the S3 resource with the integrations skill.

By the end you’ll see how the integration skill + Components + `dg` make it practical to add and configure multiple tools without drowning in setup or guesswork. The project grows step by step: raw assets (from Lesson 4) → dbt models → dbt with a transformation group → dbt plus a Sling export to S3, as in the asset graph below.

![Project with dbt and Sling](/images/ai-driven-data-engineering/lesson-5/project-dbt-sling.png)
