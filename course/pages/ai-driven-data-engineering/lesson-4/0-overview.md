---
title: "Lesson 4: Overview — Starting a Dagster project with and without skills"
module: 'ai_driven_data_engineering'
lesson: '4'
---

# Overview: Starting a Dagster project with and without skills

This is where the course becomes hands-on. You'll build the first layer of the ELT pipeline from Lesson 1's project preview: the three raw assets that load customer, order, and payment data into DuckDB. By the end of this lesson you'll have a working, validated Dagster project with a daily schedule—the foundation that Lesson 5 will build on with dbt and Sling.

But before jumping straight to the final workflow, this lesson takes a detour that's worth the time. You'll create the same project twice, once without the Dagster Expert skill, and once with it—so you can see concretely what the skill changes and why it matters. The differences aren't just cosmetic. They affect how maintainable the project is, how quickly you can debug, and how well the agent-driven workflow scales as you add more pieces.

---

## A quick note on deterministic AI

AI outputs are **not fully deterministic**. The exact commands, file layout, and code you get can vary based on the model and interface you use (e.g. Cursor, Claude Code, Windsurf), the version of the skill and of Dagster, and how the prompt is phrased.

For this course we used **Claude (claude-sonnet-4-5)** in a coding interface. Your agent may choose slightly different commands or structure; the ideas and workflow—especially "use the skill + `dg`"—stay the same regardless.
