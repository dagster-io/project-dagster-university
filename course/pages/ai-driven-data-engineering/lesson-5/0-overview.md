---
title: "Lesson 5: Integrations, Components, and AI"
module: 'ai_driven_data_engineering'
lesson: '5'
---

# Overview

In the previous lesson you built the foundation: three raw assets loading data into DuckDB with a clean, `dg`-validated project structure. Now we build on that. This lesson adds the transformation and export layers (dbt models that reshape the raw data, and a Sling component that ships the results to S3), completing the end-to-end ELT pipeline from the project preview.

Along the way you'll see two important patterns come together. The first is how Dagster Components make integrations tractable for agents: instead of figuring out how to wire dbt or Sling into a project from scratch, the agent scaffolds a predefined Component layout and fills in the specifics. The result is less ambiguity and fewer surprises. The second is skill chaining: the practice of switching between `dagster-expert` and the dbt skill as the nature of the task shifts. Knowing which skill to reach for, and when to switch, is one of the most useful habits you can develop for AI-driven Dagster work.
