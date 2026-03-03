---
title: "Lesson 2: Dagster Skills"
module: 'ai_driven_data_engineering'
lesson: '2'
---

# Dagster Skills

We maintain a collection of AI skills that give coding agents the right context and patterns for building with Dagster. We'll go into each skill in more detail later in the course; here is the overview.

## What are AI skills?

AI skills started as an [Anthropic concept](https://docs.anthropic.com/en/docs/build-with-claude/skills) for giving Claude structured, task-relevant guidance. The idea has since been adopted by other coding agents (e.g. Cursor, Windsurf, Codex) via formats like [Agent Skills](https://agentskills.io/home). A skill is essentially a bundle of instructions and references that tell the agent *when* to use *what* context so it stays on task and follows your preferred patterns.

## The Dagster skills we maintain

We currently maintain several skills in the [Dagster Skills repository](https://github.com/dagster-io/skills):

- `dagster-expert`: expert guidance for building production-quality Dagster projects. It covers CLI usage (especially `dg`), asset patterns, automation strategies (schedules, sensors, declarative automation), and implementation workflows. This skill is the main one for "how to build and structure a Dagster project" and uses the CLI heavily for scaffolding and validation.
- `dignified-python`: production-quality Python coding standards for modern Python. Use it for general Python quality (types, exceptions, API design, etc.), not for Dagster-specific patterns. It's the same standard we use internally when writing Python.

The industry is still in the early stages of developing and structuring skills. Some prefer to make skills very specific and you will see projects that have dozens of skills on a single topic. We have found benefits in building around a single skill (`dagster-expert`) which contains all the information for working with Dagster. Our `dignified-python` skill (which we will discuss later in the course) is broken out because it is non-Dagster-specific. But we will cover when it is useful to use this skill when working with Dagster.