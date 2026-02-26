---
title: "Lesson 5: Adding dbt"
module: 'ai_driven_data_engineering'
lesson: '5'
---

# Adding dbt

The raw assets are working: three DuckDB tables with customer, order, and payment data loaded and ready. That's a solid foundation, but it's not useful to anyone yet. Raw data needs cleaning, standardizing, and joining before analysts can work with it. That's what the transformation layer is for, and dbt is the right tool for it.

Most of the time you'd integrate an *existing* dbt project into Dagster—your team already has models, and you're connecting them to an orchestration layer. Here we're generating the entire dbt project from scratch alongside the Dagster integration, which gives you a useful demonstration: with a single prompt, the agent scaffolds both sides of the connection, wired together correctly from the start.

## Why switch to `/dagster-integrations`

Up to this point you've been using `/dagster-expert` for everything—project structure, assets, resources, the `dg` workflow. That's the right skill for Dagster's core abstractions. But adding dbt is primarily an integration question: how does `dagster-dbt` work, what does the dbt Component expect, how does a dbt project get wired to Dagster assets? That's the domain of `/dagster-integrations`.

This is the first example of skill chaining in this lesson—switching from the expert skill to the integrations skill at the natural seam between "Dagster structure" and "connecting an external tool." The integrations skill has deep context on `DbtProjectComponent` that the expert skill doesn't; using the right one here is what makes the agent's output trustworthy.

## The prompt

Give the agent a clear goal in terms of data products—what models you want, what format, what dependencies:

```bash {% obfuscated="true" %}
> /dagster-integrations Add a dbt project that models the data from the three raw data assets. Each raw asset should map to a corresponding dbt model in the traditional stg_ format, and the dbt models should be dependent on the raw assets.
```

Notice the prompt describes the asset graph you want, not the code. Staging models for each raw table, with the dependency wiring explicit. The agent figures out the mechanics.

## What the agent does

The integrations skill steers the agent toward the `DbtProjectComponent` rather than hand-rolling dbt wiring in Python. It starts by installing the dependency:

```bash
uv add dagster-dbt
```

Then it scaffolds the Component with `dg`, which creates the expected layout so Dagster can load your dbt project and turn models into assets:

```bash
dg scaffold defs dagster_dbt.DbtProjectComponent jaffle_shop --project-path dbt_project
```

With the Component in place, the agent creates the dbt project itself—`stg_customers`, `stg_orders`, and `stg_payments` in the traditional staging format, each reading from its corresponding raw DuckDB table. Throughout this process it alternates between `dg` and `dbt` commands so that structure and validity are confirmed at each step rather than all at once at the end:

```bash
dbt parse --project-dir dbt_project --profiles-dir dbt_project
```

When `dbt parse` succeeds, the project compiles cleanly and Dagster can load it as assets.

## What you see in the UI

Open the asset catalog. The three raw assets you built in Lesson 4 are still there—and now there are three new assets sitting downstream of them: `stg_customers`, `stg_orders`, `stg_payments`.

![Asset graph with raw assets and dbt models](/images/ai-driven-data-engineering/lesson-6/project-dbt.png)

This is the lineage the prompt described, now visible in the graph. The raw assets feed into the staging models exactly as you asked. A new team member looking at this catalog would immediately understand the pipeline's shape—not from reading the code, but from looking at the graph.

There's still some cleanup to do: the dbt assets and raw assets share the same unlabeled space in the catalog, and the dependency wiring between them could be made more explicit. That's what the next section covers.

## If something goes wrong

The `dagster-integrations` skill handles setting up the integration; the `dagster-expert` skill handles debugging. If a materialization fails, switch skills:

```bash {% obfuscated="true" %}
> /dagster-expert Help me debug my failed materialization
```

The agent can inspect logs, definitions, and resource config to fix path issues, dependency wiring, or dbt profile problems. That handoff—integrations to configure, expert to debug—is itself an example of skill chaining, and a preview of the pattern you'll use throughout this lesson.
