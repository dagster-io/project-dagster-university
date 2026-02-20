---
title: "Lesson 4: Comparing the code"
module: 'ai_driven_data_engineering'
lesson: '4'
---

# Comparing the code

You've now created the same project twice: once without any Dagster-specific guidance and once with the Dagster Expert skill. The high-level goal was identical both times—scaffold a project and add three assets that load CSVs into DuckDB. But the results look meaningfully different.

**Without the skill:**

![Project without the skill](/images/ai-driven-data-engineering/lesson-4/project-without-skills.png)

**With the Dagster Expert skill:**

![Project with the skill](/images/ai-driven-data-engineering/lesson-4/project-with-skills.png)

---

## Without the skill

The project creation command is typically the older `dagster project scaffold --name university`, which produces a flat layout: `university/university/` with a single `assets.py` and a single `definitions.py`. Assets get added by editing that file directly. There's no `dg`, no `defs/` structure, and no habit of running `dg check defs`—so definition load errors only surface when you open the UI or run something.

The result works. But it's ad hoc: file placement is whatever the agent inferred, dependencies may or may not be handled consistently, and there's no structural foundation to build on as the project grows.

---

## With the Dagster Expert skill

The project creation command is `uvx create-dagster project university --uv-sync`—the modern, recommended approach. You get a `src/university/` layout with `pyproject.toml`, `uv` for dependencies, and a clear `defs/` structure: assets under `defs/assets/`, shared resources in `defs/resources.py`, and a single `definitions.py` that composes them.

New assets are added with `dg scaffold defs ...` rather than by editing a file by hand, so they land in the right place. Dependencies are installed via `uv add`. After every change, the agent runs `dg check defs` to confirm definitions load before moving on. When the check passes, the skill suggests the next step: `dg launch --assets "..."` to run the assets and verify the runtime behavior.

---

## What the difference means in practice

The without-skill project requires you to know where things go. The with-skill project encodes that knowledge in the CLI and skill, so you don't have to.

That sounds small, but it compounds. When you add dbt models in Lesson 5, the agent will scaffold a Component layout that fits naturally into the existing `defs/` structure. When you add a schedule, it goes in `defs/schedules.py`. The project stays organized not because you're carefully maintaining it, but because the skill and `dg` consistently make the same choices.

The without-skill path can be corrected—you could reorganize a flat project into a `defs/` layout manually. But that's work you don't need to do if the agent gets the structure right from the start.
