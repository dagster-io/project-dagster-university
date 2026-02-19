---
title: "Lesson 4: Comparing the code"
module: 'ai_driven_data_engineering'
lesson: '4'
---

# Comparing the code

Here’s a concise comparison of the two approaches: **without** the skill vs **with** the Dagster Expert skill. The asset graph and project structure reflect the difference: without the skill you get a minimal, flat layout; with the skill you get a clear defs-based layout and consistent use of `dg`.

**Without the skill:**

![Project without the skill](/images/ai-driven-data-engineering/lesson-4/project-without-skills.png)

**With the Dagster Expert skill:**

![Project with the skill](/images/ai-driven-data-engineering/lesson-4/project-with-skills.png)

---

## Without the skill

- **Project creation:** Often uses `dagster project scaffold --name university`, yielding a flat layout (`university/university/` with `assets.py`, `definitions.py`).
- **Layout:** Single `assets.py` (and maybe `resources` inline); no standard `defs/` structure.
- **Dependencies:** The agent may or may not use `dagster-duckdb` or your preferred package manager; behavior varies by model and context.
- **Validation:** No built-in habit of running `dg check defs`; you may discover load errors only when you run or open the UI.
- **Scaffolding:** New assets are typically added by editing `assets.py` by hand; file placement is whatever the agent infers.

You still get a working pipeline, but structure and tooling are ad hoc.

---

## With the Dagster Expert skill

- **Project creation:** Uses `uvx create-dagster project university --uv-sync`, giving a modern layout with `src/university/`, `pyproject.toml`, and `uv`.
- **Layout:** Clear `defs/` layout: `defs/assets/`, `defs/resources.py`, and a single `definitions.py` that composes them.
- **Dependencies:** The skill steers the agent to add integrations (e.g. `uv add dagster-duckdb`) in a consistent way.
- **Validation:** The agent runs `dg check defs` after changes, so definition load errors are caught early.
- **Scaffolding:** New code is added via `dg scaffold defs ...`, so files land in the right places and the agent needs less context to “guess” structure.
- **Next steps:** The skill suggests follow-up commands (e.g. `dg launch --assets "..."`) so you can run and verify quickly.

Net effect: same high-level task (project + three DuckDB-loading assets), but with consistent structure, use of `dg`, and a workflow that scales to more assets, jobs, and schedules. The skill + `dg` combination is what makes the “with skill” path more predictable and maintainable.
