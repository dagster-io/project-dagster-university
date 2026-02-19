---
title: "Lesson 2: Other agents (Windsurf and more)"
module: 'ai_driven_data_engineering'
lesson: '2'
---

# Other agents (Windsurf and more)

If you’re using **Windsurf**, **OpenCode**, or another AI coding agent that supports the [Agent Skills](https://agentskills.io/home) format, you can still follow this course. The goal is the same: install the [Dagster skills](https://github.com/dagster-io/skills) and ensure they’re enabled so the agent has the right context for building with Dagster.

---

## 1. Install your agent

Install and sign in to your agent (e.g. Windsurf, or another Agent Skills–compatible tool) using its official setup guide.

---

## 2. Add the Dagster skills

Agents that support Agent Skills typically let you add skills from a repo or a local path:

- **CLI:** Some tools support a command like `npx agent-skills install dagster-io/skills` (or a similar `npx`/CLI command). Check your agent’s docs for “skills” or “Agent Skills” to see the exact syntax.
- **Config file:** For example, Windsurf can list skills in `.windsurf/skills.json` or load them via Cascade; add a reference to the Dagster skills repo or the skill names so the agent can fetch them.
- **Manual:** Clone or copy the [Dagster skills](https://github.com/dagster-io/skills) repository. Place the skill folders (each containing a `SKILL.md`) in the directory your agent uses for skills (e.g. a “skills” or “agent-skills” folder in the app config or project). Restart or refresh the agent so it picks up the new skills.

Use whichever method your agent documents for adding external skills.

---

## 3. Ensure the Dagster skills are enabled

In your agent’s settings or skill list, confirm that the Dagster skills are **enabled** or active. You want at least:

- **dagster-expert** — for project structure, `dg` CLI, and Dagster patterns  
- **dagster-integrations** — for adding and configuring integrations (e.g. dbt, Sling)  
- **dignified-python** (optional) — for Python best practices  

How you invoke them (e.g. by name in the prompt, or via a slash command) depends on the agent; the [Dagster skills README](https://github.com/dagster-io/skills) may have agent-specific notes.

---

## You’re set

Once the Dagster skills are installed and enabled, you’re ready for Lesson 3. The course workflow (invoke the skill, use `dg`, follow the prompts) is the same across agents; only the setup steps differ. If your agent’s docs mention “Agent Skills” or “skills directory,” use that path to add and enable the Dagster skills, then continue with the course.
