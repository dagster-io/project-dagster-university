---
title: "Lesson 3: Project setup"
module: 'ai_driven_data_engineering'
lesson: '3'
---

# Overview

This lesson gets you ready to follow the rest of the course. Pick the page that matches your AI coding agent and follow the steps to install the Dagster skills and confirm they're enabled.

## Works with any AI coding agent

The course is designed to work with any agent that supports skills. The only requirement is that your agent can load and use the [Dagster skills](https://github.com/dagster-io/skills). Those skills give the agent the right context to build Dagster projects with `dg`, follow best practices, and use integrations.

We provide short setup pages for the main options:

- [**Claude Code**](/ai-driven-data-engineering/lesson-3/1-claude): Install the Dagster skill via the plugin marketplace.
- [**Codex**](/ai-driven-data-engineering/lesson-3/2-codex): add the Dagster skills via the `npx skills` command.
- [**Cursor**](/ai-driven-data-engineering/lesson-3/3-cursor): add the Dagster skills via the `npx skills` command.
- [**GitHub Copilot**](/ai-driven-data-engineering/lesson-3/4-github-copilot): add the Dagster skills via the `npx skills` command.

Pick the page that matches your agent and follow the steps. Once the Dagster skills are installed and enabled, you're ready to move on to Lesson 4.

## Non-deterministic behavior

Coding with an AI agent is non-deterministic. The code and commands you get may differ slightly from the examples in this course depending on:

- The agent and model you use (e.g. Claude Code with Sonnet 4.6, Cursor with a different model)
- The version of the Dagster skills
- How you phrase your prompts

The course examples use Claude Code with Sonnet 4.6. If you use another agent or model, the workflow stays the same even if the exact output varies.
