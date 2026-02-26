---
title: "Lesson 3: The dg CLI"
module: 'ai_driven_data_engineering'
lesson: '3'
---

# The dg CLI

We built `dg` before AI-driven workflows really took off. It was our attempt to help you scaffold, build, and design Dagster projects with a CLI that encodes opinionated choices about project structure and patterns so you get the most out of Dagster.

## What dg does

The `dg` CLI gives you deterministic, actions over your Dagster project. Instead of having an agent guess where to put files or how to validate definitions, it can call `dg` and get consistent, correct behavior.

Key command groups:

- `dg scaffold` — Scaffold Dagster entities (e.g. assets, components), GitHub Actions workflows, and build artifacts. For example, `dg scaffold defs dagster.asset assets/my_asset.py` creates a new asset file in the right place under your project’s `defs/` folder.
- `dg dev` — Start a local Dagster instance. Run from a project directory to launch that project, or from a workspace directory to launch all projects in the workspace.
- `dg check` — Check the integrity of your Dagster code: validate definitions (`dg check defs`), TOML config (`dg check toml`), and `defs.yaml` files (`dg check yaml`). Non-zero exit codes when validation fails make it easy for agents and CI to detect errors.
- `dg list` — List Dagster entities in the current environment: definitions (`dg list defs`), components, projects, env vars, and more. Useful for agents to confirm what’s registered after making changes.
- `dg launch` — Launch a Dagster run (e.g. by asset selection, job, or partition). Lets agents trigger runs in a consistent way instead of hand-rolling run launcher code.

## Dagster Components and dg

Dagster Components work hand-in-hand with `dg` to let you build pipelines in a lightweight way. [Components](https://docs.dagster.io/guides/build/components) provide an intelligent project layout that scales from “Hello world” to advanced projects, plus ready-made component types for many common integrations. You use `dg` to scaffold and populate projects with these components—so instead of writing lots of boilerplate by hand, you get a structured layout and reusable building blocks that `dg` knows how to create and validate.

For more advanced use cases, Components also offer a class-based interface for constructing Dagster definitions from data (e.g. third-party config files) and support for YAML-based DSLs, so you can define component instances with little or no Python. This becomes especially clear later when we discuss working with integrations: the combination of `dg` and Components is what makes it practical to add and configure integrations without drowning in setup code.

## Why it matters for AI-driven workflows

With `dg`, an agent doesn’t have to infer project layout or which APIs to call. It can:

- Scaffold new assets or other definitions in the correct location
- Validate that definitions load and pass checks
- List what’s defined and launch runs

That keeps behavior predictable and aligned with how we recommend structuring Dagster projects. We’ll see in later sections how the Dagster Skills use `dg` as the primary way to interact with your project.

For full command options and subcommands, see the [dg CLI reference](https://docs.dagster.io/api/clis/dg-cli/dg-cli-reference) in the Dagster docs.
