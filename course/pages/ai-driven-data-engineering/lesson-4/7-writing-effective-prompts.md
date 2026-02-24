---
title: "Lesson 4: Writing effective prompts"
module: 'ai_driven_data_engineering'
lesson: '4'
---

# Writing effective prompts

The skill shapes how the agent behaves, but you decide what to ask for. A well-framed prompt produces reliable, targeted output. A poorly framed one makes the agent invent structure, misinterpret scope, or produce code that works but doesn't fit the project. These patterns apply to any agent, any skill.

---

## Describe outcomes, not code

The most reliable prompts describe what data should exist and how it should relate to other data—not the code you want written. You already saw this in the assets discussion: Dagster and the agent share a vocabulary around data products.

That principle generalizes to all prompts:

**Mechanical (less reliable):**
```
Write a Python function that downloads a CSV from a URL and inserts the rows into DuckDB
```

**Outcome-oriented (more reliable):**
```
Create an asset that loads the raw orders CSV from [URL] into a DuckDB table called raw_orders, in the same group as the other raw assets
```

The second prompt defines what should exist (an asset, in a specific group, loading a specific table) and leaves the mechanics to the agent and skill. That's also what lands in the asset catalog, which makes the result immediately verifiable.

---

## Scope to one deliverable

A prompt that asks for too much forces the agent to make too many decisions at once, and the risk of inconsistent choices compounds with each additional decision. If you want a new integration, a refactored resource, and a schedule update, those are three separate prompts—not one.

The right unit of a prompt is roughly: *one thing I can verify when it's done*. Adding a new asset, connecting dbt to the raw assets, or fixing a specific error are all well-scoped. "Improve the project" or "finish the pipeline" are not.

When a task genuinely requires multiple pieces, reach for plan mode first (lesson 7). Plan mode handles the coordination; individual prompts should still be scoped.

---

## Include what the agent would otherwise have to infer

You don't need to explain everything—the skill covers Dagster conventions, `dg` handles scaffolding, and `dg check defs` catches structural errors. What you *do* need to include is anything project-specific that isn't visible from the codebase alone:

- **Which convention to follow**, when you've established one: "use the `_make_raw_asset()` factory like the other raw assets"
- **What not to change**: "only update `resources.py`—don't touch the asset files"
- **Explicit constraints**: "the DuckDB path should stay at `data/staging/data.duckdb`"
- **The expected output**: "the asset should appear in the `ingestion` group, not `default`"

These aren't explanations—they're constraints that narrow the decision space and prevent the agent from defaulting to a different valid interpretation.

---

## Correct mistakes precisely

When the agent gets something wrong, a targeted correction is more effective than a vague "that's not right, try again." Vague corrections send the agent back to the same broad decision space that produced the original problem.

**Vague:**
```
That's not right, try again
```

**Targeted:**
```
The new asset is missing the _make_raw_asset() factory—it defines the function directly
instead of using the factory. Fix only that; don't change the DuckDB path or group name.
```

The targeted version names what's wrong, what the correct pattern is, and what should *not* change as a side effect of the fix. That last part matters: without it, the agent may "fix" the issue while inadvertently changing something that was correct.

---

## Don't describe the external tool when asking about Dagster

A common mistake when working with integrations: explaining the external tool's API in the prompt when the integrations skill already has that context.

**Over-explained:**
```
/dagster-integrations I want to add Sling to export data. Sling uses a YAML replication
config with source and target fields, and a streams section that maps table names to
destination paths. Please set this up.
```

**Let the skill do its job:**
```
/dagster-integrations Set up a Sling component that exports fct_orders from DuckDB to S3
as a Parquet file. The bucket is called test-bucket.
```

Describing what you want the outcome to look like (what table, what destination, what format) is useful. Describing how Sling works internally is noise—the skill knows that already, and redundant context can lead the agent to weight your description over its own more accurate understanding.
