---
title: "Lesson 4: How a skill works"
module: 'ai_driven_data_engineering'
lesson: '4'
---

# How a skill works

Before we create the same project *with* the Dagster Expert skill, it helps to know what a skill is and how the agent uses it.

---

## What skill files look like

A **skill** is a structured document (often a `SKILL.md` or similar file) that your coding agent can load when it sees a relevant trigger—e.g. you type `/dagster-expert` or mention “Dagster” in the prompt. The skill file typically includes:

- **When to use the skill** — Triggers, slash commands, or intent phrases (e.g. “create a Dagster project”, “add a schedule”).
- **Instructions** — What to do first (e.g. use `dg` for scaffolding, run `dg check defs` after changes).
- **References** — Pointers to CLI commands, project layout, and patterns (e.g. use `uvx create-dagster`, put assets under `defs/assets/`, use `DuckDBResource` from `dagster-duckdb`).

The agent doesn’t “run” the skill like a script; it **reads** the skill as context and uses that to decide which commands to run and how to structure code.

---

## How skills are used

When you invoke the skill (e.g. `/dagster-expert create a new Dagster project called university`):

1. The interface or agent matches your prompt to the skill (e.g. “dagster-expert” or “Dagster project”).
2. The skill’s content is added to the context sent to the model.
3. The model follows the skill’s instructions: use `dg` and the recommended layout, run `dg check defs` after scaffolding, add dependencies with `uv`, etc.

So the same high-level request (“create a project”, “add three assets”) leads to **different, more opinionated behavior** when the skill is active: the agent prefers `dg` over hand-written structure and validates with `dg check defs`. Next we’ll see that in practice by creating the project again with the skill.
