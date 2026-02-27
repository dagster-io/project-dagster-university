---
title: "Lesson 2: The Dagster CLIs"
module: 'ai_driven_data_engineering'
lesson: '2'
---

# The Dagster CLIs

We built CLI tooling before AI-driven workflows really took off. It was our attempt to assist with scaffolding, building, and designing Dagster projects with a CLI that encodes opinionated choices about project structure and patterns so you get the most out of Dagster.

## create-dagster CLI (bootstrapping)

The first step in building with Dagster is building a project. The [create-dagster CLI](https://docs.dagster.io/api/clis/create-dagster) is the official way to scaffold that initial structure:

- `create-dagster project` — Scaffold a new Dagster project at a given path. Creates `src/PROJECT_NAME/` with `definitions.py`, a `defs/` directory.
- `create-dagster workspace` — Initialize a new Dagster workspace with a `projects/` folder, `deployments/local/`, and a root `dg.toml`. Use this when you want to manage multiple projects in one repo.

Run from an empty directory or pass `.` to create in the current directory. For installation and full options, see the [create-dagster CLI reference](https://docs.dagster.io/api/clis/create-dagster).

## dg CLI (developing)

The `dg` CLI gives you deterministic actions over your Dagster project. Instead of having to guess where to put files or how to validate definitions, `dg` offers consistent, correct behavior.

There are a number of [`dg` commands](https://docs.dagster.io/api/clis/dg-cli/dg-cli-reference):

- `dg scaffold`: scaffold Dagster entities (e.g. assets, components), GitHub Actions workflows, and build artifacts.
- `dg dev`: start a local Dagster instance.
- `dg check`: check the integrity of your Dagster code.
- `dg list`: list Dagster entities in the current environment.
- `dg launch`: launch a Dagster run (e.g. by asset selection, job, or partition).
- `dg api`: make REST-like API calls to Dagster Plus (agents, assets, deployments, runs, logs, schedules, sensors, secrets, and more).
- `dg plus`: commands for interacting with Dagster Plus—login, deploy (build and push, configure, start/finish), create (e.g. CI API tokens, env vars), and pull (e.g. env from cloud).

## Dagster Components (integrate)

Dagster Components work hand-in-hand with `dg` to let you build pipelines in a lightweight way. [Components](https://docs.dagster.io/guides/build/components) provide an easy interface for designing Dagster applications as well as prebuilt solutions for many common integrations.

## Why it matters for AI-driven workflows

Instead of writing Dagster code directly, using `dg` and Components allows for a more consistent coding experience and makes it easier to do common things like:

- Scaffold new assets or other definitions in the correct location
- Validate that definitions load and pass checks
- List what's defined and launch runs

That keeps behavior predictable and aligned with how we recommend structuring Dagster projects. We'll see in later sections how the Dagster Skills use `dg` as the primary way to interact with your project.
