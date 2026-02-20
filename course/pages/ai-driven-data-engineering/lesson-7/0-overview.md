---
title: "Lesson 7: Overview — Extend the project"
module: 'ai_driven_data_engineering'
lesson: '7'
---

# Extend the project

You've built a complete ELT pipeline from scratch: raw data into DuckDB, dbt models transforming it into something useful, a Sling export shipping the results to S3, data quality checks, a daily schedule, and clean Python throughout. All from prompts.

This lesson doesn't introduce new concepts. It's an open invitation to keep going.

The best way to solidify an AI-driven workflow is to use it on something you actually care about—or at least something that makes you think. So this lesson offers a set of extension ideas and, more importantly, a way of approaching them when you're not sure what to ask for.

---

## The workflow is the same

Whatever you choose to build next, the approach doesn't change:

Describe the data product or behavior you want. Think about whether the task is about Dagster itself (reach for `/dagster-expert`) or about connecting an external tool (reach for `/dagster-integrations`). Let the agent figure out the mechanics. Check the result in the asset catalog.

The only new challenge is that some of the things you might want to build have names in Dagster that you don't know yet—and that's fine.

---

## You don't need to know the abstraction to ask for it

One of the most useful things you can do with a skill-equipped agent is describe what you want in plain English, without knowing the right Dagster term. The skill will figure it out.

For example: say you want your raw assets to process data one month at a time so you can backfill a year of history without running everything in a single job. You might not know that Dagster calls this **partitions**. That's not a problem. Just describe it:

```
/dagster-expert I want each of my raw assets to process data for a specific month, so I can backfill the last 12 months one month at a time. How do I set this up?
```

The agent will explain what partitions are, show you how they apply to your project, and scaffold the changes. By the end of the conversation you'll understand the abstraction because you learned it in the context of your actual pipeline—not from a documentation page in the abstract.

This is how the lower learning curve benefit from Lesson 1 actually works in practice: you describe intent, the agent maps it to the right abstraction, and you understand it by seeing it applied.
