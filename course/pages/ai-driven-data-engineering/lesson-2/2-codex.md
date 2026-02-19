---
title: "Lesson 2: Codex"
module: 'ai_driven_data_engineering'
lesson: '2'
---

# Codex

If you’re using **Codex** as your AI coding agent, you need to install and enable the Dagster skills so the agent has the right context for building with Dagster. The steps below assume Codex’s skill system (e.g. `/learn` or skills in `~/.codex/skills/`); adjust if your Codex version uses a different flow.

---

## 1. Install Codex

Install Codex from the official setup guide for your environment and sign in.

---

## 2. Add the Dagster skills

Codex can load skills from a repository or from a local skills directory. To use the Dagster skills:

- **From the skill registry:** If Codex supports adding skills by name, add `dagster-io/skills` (or the individual skills such as `dagster-expert`, `dagster-integrations`) so the agent can load them when you invoke the skill in a prompt.
- **Manual install:** Clone or copy the [Dagster skills](https://github.com/dagster-io/skills) repository (or the relevant skill folders containing `SKILL.md`) into your Codex skills directory (often `~/.codex/skills/`). Restart or refresh Codex so it picks up the new skills.

Check Codex’s current documentation for the exact command or path (e.g. `/learn @dagster-io/skills` or a settings-based install).

---

## 3. Ensure the Dagster skills are enabled

In Codex settings or the skill list, confirm that the Dagster-related skills are **enabled**. You want at least:

- **dagster-expert** — for project structure, `dg` CLI, and Dagster patterns  
- **dagster-integrations** — for adding and configuring Dagster integrations (e.g. dbt, Sling)  
- **dignified-python** (optional) — for general Python quality

Once they’re enabled, you can invoke them in your prompts (e.g. by name or with the `$skill-name` syntax if your version supports it).

---

## You’re set

With the Dagster skills installed and enabled, you’re ready for Lesson 3. In later lessons you’ll use the skills so the agent follows Dagster best practices and uses `dg` for scaffolding and validation.
