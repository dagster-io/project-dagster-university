---
title: "Lesson 1: Thinking in assets"
module: 'ai_driven_data_engineering'
lesson: '1'
---

# Thinking in assets

There's a reason Dagster and AI-driven development fit together so naturally, and it comes down to how people actually describe what they want.

When a data engineer explains a pipeline to a colleague, they rarely talk about code. They say things like: "we need a clean customers table that comes from the raw CRM export," or "the weekly orders summary should wait until payments are reconciled." They're describing *data products* and their relationships—not steps in a script. That turns out to be almost exactly how people write prompts too.

---

## Assets as a natural vocabulary

Dagster models data work as **assets**: tables, files, models, and other data objects that have explicit lineage and dependencies. An asset isn't "run this code"; it's "this data exists, it was produced by this logic, and it depends on these upstream sources." When something changes, Dagster knows which downstream assets are stale and what needs to run.

This creates a shared vocabulary between you, Dagster, and the AI. When you write a prompt like:

> Create an asset that loads raw customer data from this CSV into a DuckDB table

...you're not asking for a function. You're describing a data product you want to exist in the world. Dagster models it the same way. The agent translates that description into a properly declared Dagster asset—with the right name, the right resource connection, and the right place in the project structure—because both you and Dagster are thinking about the same thing.

---

## The agent organizes the catalog better than you might expect

One of the less obvious benefits of this workflow is what happens to the asset catalog as your project grows.

When engineers write pipelines by hand, organization tends to slip. Assets end up with inconsistent naming, missing group assignments, and undocumented dependencies between layers. The catalog becomes hard to navigate. Everyone on the team knows what the pipeline does because they wrote it; a new person has to reverse-engineer it from the code.

When you build with an agent and the Dagster skill, something different happens. Because you describe data products in your prompts—"the dbt staging models should be in a transformation group," "the Sling export should depend on fct_orders"—the agent materializes those relationships directly into the asset graph. The dependencies are explicit from the first prompt. The groups are named intentionally. The lineage is correct because you described it that way before a single line of code was written.

The result is an asset catalog that legibly represents your data model, not one that accumulated by accident.

---

## What this means in practice

As you work through this course, try framing prompts in terms of what data you want to exist and how it should relate to other data—not in terms of the code you want written.

Instead of:
```
> Write a function that queries DuckDB and uploads to S3
```

try:

```
> Create an asset that reads from the `fct_orders` table and exports it to S3 as Parquet, dependent on `fct_orders`
```

Both prompts might produce working code. The second one produces working code *and* a correctly wired asset graph, because the intent was clear from the start.

That's the mental shift. When you and the agent are both thinking about the same asset graph, the conversation is cleaner, the results are more predictable, and the project stays organized as it grows.
