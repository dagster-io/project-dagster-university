---
title: "Lesson 4: Writing effective prompts"
module: 'ai_driven_data_engineering'
lesson: '4'
---

The workflow you've seen in this lesson - building assets, debugging failures, adding automation - depends on how well you direct the agent. The mechanics of prompting are simple. The discipline is harder.

These principles apply across tools, but the examples here are grounded in the Dagster project you've been building.

## Describe the data product, not the code

Tell the agent what the pipeline should produce, not which class to instantiate. The agent knows the mechanics; you supply the goal.

Instead of:

```
Write a DbtProjectComponent that points at a dbt project.
```

Try:

```
Add a dbt project that models the data from the three raw assets.
Each raw table maps to a stg_ staging model.
```

The first version delegates your thinking to the agent and risks getting back boilerplate that doesn't fit your project. The second gives the agent a clear outcome to work toward.

## Use the right skill prefix

The skill prefix determines which context the agent draws from when generating code.

- `/dagster-expert` - Dagster core concepts: assets, jobs, schedules, resources, debugging
- `/dagster-integrations` - Connecting external tools: dbt, Sling, S3, and other integrations

Using the wrong skill doesn't break anything, but the agent is working from thinner context for the task at hand. If you're debugging a partitioned asset, use `/dagster-expert`. If you're wiring up a dbt project, use `/dagster-integrations`.

## Include verification in the prompt

Make validation a required step, not something that happens if you remember to ask. Build it into the prompt directly:

```
Add a daily schedule that targets the ingestion job.
Confirm with `dg check defs` after making changes.
```

This closes the trust-then-verify gap. The agent won't skip validation if you've made it part of the task. Without this, you may not catch a broken definition until you try to load the UI or run a job.

## Scope one thing at a time

Combining multiple changes into one prompt produces a large, hard-to-debug result.

Instead of:

```
Add a dbt project, connect it to the raw assets, and write tests for the staging models.
```

Break it into steps:

```
Step 1: Add a dbt project with staging models for the three raw assets.
Step 2: (after validating) Connect the dbt assets to the raw assets as upstream dependencies.
Step 3: (after validating) Add schema tests to the staging models.
```

Each step ends with a `dg check defs` before the next one starts. This keeps the blast radius small and makes failures easy to locate. If something breaks after step 2, you know exactly where to look.

## Lead with context the agent doesn't have

The agent knows Dagster patterns. It doesn't know your project's specifics. State constraints upfront rather than correcting after the fact.

```
The raw CSV is at https://example.com/data/orders.csv.
The target table is raw_orders in DuckDB at data/staging/data.duckdb.
Use the _make_raw_asset() factory like the other raw assets in the project.
Add an asset that ingests this file.
```

Compare that to a prompt that leaves out the factory convention and requires a follow-up correction. Context at the start of a prompt is more reliable than correction at the end, especially as a session grows longer and earlier context fades.

## Ask for a plan before complex changes

For tasks that touch more than two or three files, start with a planning step before any code is written:

```
Before implementing, draft a plan for adding Sling ingestion for the orders table.
List each file that will be created or modified.
```

Review the plan, ask questions, push back if something looks off. Only then give the go-ahead. This gives you a checkpoint before changes are made and catches misunderstandings early. The planning workflow is covered in more depth in Lesson 8.
