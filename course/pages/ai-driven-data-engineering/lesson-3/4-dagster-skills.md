---
title: "Lesson 3: Dagster Skills"
module: 'ai_driven_data_engineering'
lesson: '3'
---

# Dagster Skills

We maintain a collection of **AI skills** that give coding agents the right context and patterns for building with Dagster. We’ll go into each skill in more detail later in the course; here is the overview.

---

## What are AI skills?

AI skills started as an [Anthropic concept](https://docs.anthropic.com/en/docs/build-with-claude/skills) for giving Claude structured, task-relevant guidance. The idea has since been adopted by other coding agents (e.g. Cursor, Windsurf, Codex) via formats like [Agent Skills](https://agentskills.io/home). A skill is essentially a bundle of instructions and references that tell the agent *when* to use *what* context so it stays on task and follows your preferred patterns.

---

## The three main Dagster skills

We currently maintain three main skills in the [Dagster Skills repository](https://github.com/dagster-io/skills):

- **`dagster-expert`** — Expert guidance for building production-quality Dagster projects. It covers CLI usage (especially `dg`), asset patterns, automation strategies (schedules, sensors, declarative automation), and implementation workflows. This skill is the main one for “how to build and structure a Dagster project” and uses the CLI heavily for scaffolding and validation.

- **`dagster-integrations`** — A broad catalog of 82+ Dagster integrations (AI/ML, ETL, storage, validation, etc.). It helps the agent pick the right integration, initialize it, and configure it in your project, including many of the quirks and gotchas you’d hit in real use.

- **`dignified-python`** — Production-quality Python coding standards for modern Python. Use it for general Python quality (types, exceptions, API design, etc.), not for Dagster-specific patterns. It’s the same standard we use internally when writing Python.

We’ll talk about each skill in more detail in later lessons. For a quick start with AI-assisted Dagster development, see [AI-assisted development with Dagster Skills](/shared/dagster-skills) in the shared course content.
