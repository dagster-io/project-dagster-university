---
title: "Lesson 5: Adding dbt"
module: 'ai_driven_data_engineering'
lesson: '5'
---

# Adding dbt

Usually you integrate an **existing** dbt project into Dagster. Here we’ll generate a dbt project from scratch based on the three raw assets from Lesson 4 (raw_customers, raw_orders, raw_payments), using the **`dagster-integrations`** skill and the dbt Component.

---

## The prompt

Give the agent a clear goal and use the integration skill:

```bash
/dagster-integrations Add a dbt project that models the data from the three raw data assets. Each raw asset should map to a corresponding dbt model in the traditional stg_ format, and the dbt models should be dependent on the raw assets.
```

The skill focuses on the integration ecosystem and knows how to scaffold the **dbt Component** with `dg`.

---

## What the agent does

1. **Add dependencies** — It installs the Dagster dbt integration (and any related packages, e.g. Sling if needed later):

   ```bash
   uv add dagster-sling dagster-dbt
   ```

2. **Scaffold the dbt Component** — Instead of hand-rolling dbt wiring, it uses `dg` to add the dbt Component. The component type is `dagster_dbt.DbtProjectComponent`, and you pass a name and the path to the dbt project directory:

   ```bash
   dg scaffold defs dagster_dbt.DbtProjectComponent jaffle_shop --project-path dbt_project
   ```

   That creates the expected layout and wiring so Dagster can load your dbt project and turn models (and optionally tests) into assets.

3. **Build the dbt project** — The agent then creates the dbt project: models in the traditional `stg_` format (e.g. `stg_customers`, `stg_orders`, `stg_payments`) that read from the raw tables and are declared as depending on the raw Dagster assets. It alternates between **`dg`** and **`dbt`** commands so structure stays correct and you can validate as you go.

4. **Validate** — For example, to ensure the dbt project parses and compiles:

   ```bash
   dbt parse --project-dir dbt_project --profiles-dir dbt_project
   ```

When that succeeds, the dbt assets are properly generated and you can see them in the Dagster UI, with dependencies from the raw assets into the staging models.

![Asset graph with raw assets and dbt models](/images/ai-driven-data-engineering/lesson-5/project-dbt.png)

---

## If something goes wrong

As in Lesson 4, you can lean on the expert skill to debug:

```bash
/dagster-expert Help me debug my failed materialization
```

The agent can inspect logs, definitions, and resource config to fix path issues, dependency wiring, or dbt profile problems. The combination of **`dagster-integrations`** (to add and configure dbt) and **`dagster-expert`** (to debug runs and definitions) keeps the workflow smooth.
