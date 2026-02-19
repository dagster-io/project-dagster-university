---
title: "Lesson 4: Overview — Starting a Dagster project with and without skills"
module: 'ai_driven_data_engineering'
lesson: '4'
---

# Overview: Starting a Dagster project with and without skills

This lesson shows the **point of agent skills**: how they improve building with Dagster and why the skill’s integration with the `dg` CLI works particularly well. You’ll create the same small project twice—once without a skill and once with the **Dagster Expert** skill—and see how structure, tooling, and debugging differ.

---

## Why agent → CLI → skills matters

Using an agent **directly** on Dagster can work, but the agent has to guess project layout and APIs. Adding a **CLI layer** (`dg`) gives the agent deterministic actions (scaffold, check, launch). Adding **skills** on top of that gives the agent the right context so it uses `dg` and follows best practices. The progression looks like this:

**Agent only** — The agent infers how to create a project and where to put files; results vary.

![Prompt: agent only](/images/ai-driven-data-engineering/lesson-4/prompt-agent.png)

**Agent + dg** — The agent can call `dg` to scaffold and validate; behavior is more consistent.

![Prompt: agent with dg CLI](/images/ai-driven-data-engineering/lesson-4/prompt-agent-dg.png)

**Agent + dg + skill** — The Dagster Expert skill tells the agent when and how to use `dg`, so you get the recommended project layout and workflow.

![Prompt: agent with dg and skill](/images/ai-driven-data-engineering/lesson-4/prompt-agent-dg-skill.png)

In this lesson you’ll see that progression in practice, and how the resulting **project** structure differs (without skill vs with skill).

---

## What we'll cover

- **Overview of the Dagster Expert skill** — What the skill provides and when to use it.

- **A quick note on deterministic AI** — You won’t necessarily get identical outputs across agents or interfaces; we’ll call out what we used for this course.

- **Create a new project (without the skill)** — Scaffold a project and generate assets using a generic prompt, and see what the agent does by default.

- **How a skill works** — What skill files look like and how the agent uses them.

- **Create a new project (with the skill)** — Same goals, but with the `dagster-expert` skill. You’ll see the agent use `dg` and modern project layout (e.g. `uvx create-dagster`, `dg scaffold`, `dg check defs`, `dg launch`).

- **Debugging** — Using the skill to fix a real error (e.g. DuckDB path) and a callout to Dagster+ branch deployments for isolated testing.

- **Comparing the code** — Side-by-side comparison of the two approaches.

- **Dagster features** — Adding automation (e.g. scheduling) with the skill.

---

## A quick note on deterministic AI

AI outputs are **not fully deterministic**. The exact commands, file layout, and code you get can vary based on:

- The model and interface you use (e.g. Cursor, Claude Code, Windsurf)
- The version of the skill and of Dagster
- How the prompt is phrased

For this course we used **Claude (claude-sonnet-4-5)** in a coding interface. Your agent may choose slightly different commands or structure; the ideas and workflow (especially “use the skill + `dg`”) stay the same.
