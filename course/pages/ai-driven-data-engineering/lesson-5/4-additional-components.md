---
title: "Lesson 5: Additional components"
module: 'ai_driven_data_engineering'
lesson: '5'
---

# Additional components

Most likely dbt isn’t the only integration in your Dagster project. You might not even know what options exist. The **`dagster-integrations`** skill can suggest integrations and then scaffold the right Component so you stay within best practices.

---

## Asking the agent for options

Suppose you want to export the results of one of your dbt models (e.g. `fct_orders`) to S3. You could do it with a DuckDB query in an asset, but you’d prefer a proper replication path. You also want to avoid paid services and stick with open-source tools. Ask the agent:

```bash
/dagster-integrations I would like to export the data from the fct_orders model to S3. What are some good open-source tools that can handle this with Dagster?
```

```
For exporting from DuckDB to S3, there are two strong open-source options with first-class
  Dagster support:

  ---
  Sling (dagster-sling) — Recommended for this use case

  Sling is purpose-built for data replication between databases and file systems, including
  DuckDB → S3. It's the most direct fit here.

  - Reads directly from DuckDB and writes to S3 as CSV, Parquet, JSON, etc.
  - Component-based Dagster integration with a simple YAML config
  - Low complexity, high performance
  - Open-source CLI tool

  # replication config example
  source: DUCKDB
  target: S3

  streams:
    main.fct_orders:
      object: s3://my-bucket/exports/fct_orders.parquet
      mode: full-refresh

  ---
  dlt (dagster-dlt) — Best if you need schema evolution or incremental loads

  dlt is a Python-native EL library that handles schema inference, incremental state, and
  normalization. It supports DuckDB as a source and S3 as a destination.

  - More code-centric than Sling (Python-based pipeline definitions)
  - Strong incremental loading with built-in state management
  - Good fit if the export logic needs transformation or filtering in Python
  - Open-source

  ---
  Quick comparison for your case

  ┌─────────────────────┬─────────────────┬─────────────────┐
  │                     │      Sling      │       dlt       │
  ├─────────────────────┼─────────────────┼─────────────────┤
  │ DuckDB → S3         │ ✅ Native       │ ✅ Supported    │
  ├─────────────────────┼─────────────────┼─────────────────┤
  │ Config style        │ YAML            │ Python          │
  ├─────────────────────┼─────────────────┼─────────────────┤
  │ Incremental         │ ✅              │ ✅ Strong       │
  ├─────────────────────┼─────────────────┼─────────────────┤
  │ Complexity          │ Low             │ Medium          │
  ├─────────────────────┼─────────────────┼─────────────────┤
  │ Dagster integration │ Component-based │ Component-based │
  └─────────────────────┴─────────────────┴─────────────────┘

  Recommendation: Start with Sling — it's the least overhead for a straightforward DuckDB → S3
   export and integrates cleanly as a Dagster component alongside your existing dbt setup.
  Would you like to implement one of these?
```

---

## Setting up the Sling component

Once you’ve chosen Sling, ask the agent to add it:

```bash
/dagster-integrations Setup a Sling component that exports the DuckDB data from fct_orders to S3 (assume the bucket is called test-bucket).
```

The flow is similar to adding dbt:

1. **Install the dependency:**

   ```bash
   uv add dagster-sling
   ```

2. **Scaffold the Component** — The agent uses `dg` to add a Sling replication component (e.g. `SlingReplicationCollectionComponent`) with a sensible name:

   ```bash
   dg scaffold defs dagster_sling.SlingReplicationCollectionComponent fct_orders_s3_export
   ```

3. **Configure replication** — The agent fills in the replication config (source: DuckDB, target: S3, stream for `fct_orders` → e.g. `s3://test-bucket/exports/fct_orders.parquet`). You may need small tweaks (bucket name, path, format).

---

## Wiring the dependency

So that the Sling export runs only after `fct_orders` is materialized, add an asset dependency:

```bash
/dagster-integrations The parquet asset should have a dependency on the fct_orders asset.
```

The agent will wire the Sling-produced asset (e.g. the Parquet file in S3) to depend on the `fct_orders` asset. Then the graph is correct: raw → staging → fct_orders → S3 export, and you can run or schedule the full pipeline with the right order.

![Asset graph with dbt and Sling export to S3](/images/ai-driven-data-engineering/lesson-5/project-dbt-sling.png)

---

## Why this fits the lesson

You didn’t have to memorize Sling vs dlt or Component names. You described the **goal** (export fct_orders to S3, open-source), and the integration skill suggested options and then implemented one with a Component. Same pattern as dbt: **skill + `dg` + Component** keeps the agent on a narrow, well-defined path so your project stays consistent and maintainable as you add more integrations.
