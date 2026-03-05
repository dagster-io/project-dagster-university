---
title: "Lesson 5: Skill chaining"
module: 'ai_driven_data_engineering'
lesson: '5'
---

# Skill chaining

If you look back at this lesson, you'll notice you didn't use just one skill. You used the `dagster-expert` skill to scaffold and build the dbt project and Dagster Component, and you switched to dbt skill for more detailed work with the actual dbt project.

This is skill chaining: switching skills as the nature of your task shifts. Each skill has a different knowledge domain. Using the right one at the right time is what keeps the agent's output trustworthy.

## How to think about it

Use `/dagster-expert` when you're working with Dagster itself:

- Creating or scaffolding assets, schedules, sensors, jobs
- Understanding project structure and definitions
- Running or materializing assets (`dg launch`, `dg list`)
- Debugging failed runs
- Automation: conditions, partitions, backfills
- Any general Dagster concept, including asset checks and resources

Use `/dbt:using-dbt-for-analytics-engineering` when you're doing dbt-specific work:

- Writing or modifying dbt models
- Creating or updating `schema.yml` with tests and documentation
- Using `ref()` and `source()` correctly
- Running `dbt parse`, `dbt compile`, or `dbt test`
- Configuring `dbt_project.yml` and profiles

Rule of thumb: if the task is about dbt (models, schema, dbt commands), use the dbt skill. If it's about Dagster (structure, definitions, dg workflow, debugging), use `/dagster-expert`.

## The chaining pattern

Look at the switches that happened as we built this lesson:

1. `/dagster-expert` scaffolded the dbt project, created the staging models, and validated with `dbt parse`. This is a case where the Dagster skill is enough: creating the `DbtProjectComponent`, scaffolding the project layout, and wiring it into Dagster are all Dagster questions. The dbt skill adds value when you're writing or modifying dbt models directly — that comes later in the chaining sequence.

2. `/dagster-expert` handled wiring the dbt assets to the raw assets, setting group names, and validating with `dg check defs`. Once the dbt project existed as a Dagster entity, questions like "which group should these assets be in?" or "how do I make the raw assets upstream of the dbt models?" are core Dagster questions.

3. `/dbt:using-dbt-for-analytics-engineering` came back to add schema tests to the staging models. Writing `not_null` and `unique` tests in `schema.yml` is dbt work, not Dagster work.

4. `/dagster-expert` handled debugging when a materialization failed. Reading the run logs, tracing the error to a resource misconfiguration, and fixing it is Dagster debugging.

![chaining](/images/ai-driven-data-engineering/lesson-5/chaining.png)

Each switch happens at a natural seam: when the task shifts from "build this dbt project" to "wire this into Dagster" and back again.

## The natural seam

The seam between the two skills usually corresponds to a real boundary in the work. dbt models are SQL files with dbt-specific conventions. Dagster assets are Python definitions. The `DbtProjectComponent` is the bridge between them, and setting it up touches both sides.

Skill chaining isn't overhead. Each skill has deep context about its domain, and shallow context about the other's. When you're writing dbt models, the dbt skill knows far more about dbt conventions than the expert skill does. When you're debugging a failed Dagster run, the expert skill knows far more about Dagster's execution model.

The agent doesn't switch on its own. You switch it by invoking a different skill at the start of your prompt. The habit is: pause at seam points, name the skill explicitly, and the agent will follow.
