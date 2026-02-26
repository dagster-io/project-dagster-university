---
title: "Lesson 2: Project setup"
module: 'ai_driven_data_engineering'
lesson: '2'
---

# Project setup

This lesson gets you ready to follow the rest of the course. You’ll choose an AI coding agent, install the [Dagster skills](https://github.com/dagster-io/skills), and confirm they’re enabled. The course is designed to work with any of the main agent options—only the setup steps differ slightly.

## Works with any AI coding agent

The course should work with any AI coding agent that supports skills. The only requirement is that your agent can load and use the [Dagster skills](https://github.com/dagster-io/skills) from the `dagster-io/skills` repository. Those skills give the agent the right context to build Dagster projects with `dg`, follow best practices, and use our integrations.

We provide short setup pages for the main options:

- **Claude Code** — Install the Dagster skill via the plugin marketplace and confirm it’s enabled.
- **Cursor** — Add the Dagster skills (e.g. via Cursor’s skills/plugins) and ensure they’re enabled.
- **Codex** — Install skills via Codex’s skill system and enable the Dagster skills.
- **Other agents** — For Windsurf and other Agent Skills–compatible tools, install from the Dagster skills repo and enable the skills in your agent’s settings.

Pick the page that matches your agent and follow the steps to ensure the Dagster skill is enabled before you continue to Lesson 3.

---

## Non-deterministic behavior

Coding with an AI agent is non-deterministic. The code and commands you get may differ slightly from the examples in this course depending on:

- The agent and model you use (e.g. Claude Code with Sonnet 4.6, Cursor with a different model)
- The version of the Dagster skills
- How you phrase your prompts

The course examples use Claude Code with Sonnet 4.6. If you use another agent or model, you should still have a similar experience—the workflow (use the skill, use `dg`, follow the prompts) stays the same even if the exact output varies a bit. Once your agent has the Dagster skills enabled, you’re ready to move on to Lesson 3.
