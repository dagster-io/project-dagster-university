---
title: "Lesson 8: Working with an existing project"
module: 'ai_driven_data_engineering'
lesson: '8'
---

# Working with an existing project

This course has been entirely greenfield: start a new project, scaffold assets, add integrations. That's the right way to learn. But most real work happens in projects that already exist, with conventions already established, assets already written, and patterns you didn't choose.

Adding an AI-driven workflow to an existing Dagster project -- a brownfield project -- works well, but the approach differs from starting fresh. The agent doesn't arrive knowing your conventions, your naming patterns, or why certain decisions were made. Without that context, it will invent its own.

## The core challenge

In a greenfield project, the skill provides all the context the agent needs. It knows to use `uv`, to scaffold with `dg`, to use `_make_raw_asset()` factories, to put resources in the right place.

In a brownfield project, the project has its own conventions that may differ from the skill's defaults. Maybe assets use a different factory pattern. Maybe the project uses Poetry instead of `uv`. Maybe resources are structured differently than the skill expects.

The agent will follow the skill's defaults unless you give it project-specific context. Getting that context in front of the agent before it writes anything is what makes brownfield work productive.

## Start with a context file

The most effective thing you can do before prompting in a brownfield project is write down the conventions in a file your agent reads automatically. In brownfield work this is even more critical than in a new project.

Each agent has its own convention for this file:

- **Claude Code**: `CLAUDE.md` in the project root
- **Cursor**: `.cursorrules` in the project root
- **GitHub Copilot**: `.github/copilot-instructions.md`
- **Codex**: `AGENTS.md` in the project root

The content is the same regardless of tool. A good context file covers:

- Package manager and how to add dependencies
- Project structure (where assets, resources, schedules live)
- Existing patterns (factory functions, naming conventions)
- Validation commands (`dg check defs`, test runner invocation)
- What not to change (core abstractions, configuration structure)

Example:

```markdown
# Project conventions

## Package manager
Use `poetry add` (not uv). Run `poetry install` after adding dependencies.

## Project layout
Assets: `src/pipeline/defs/assets/`
Resources: `src/pipeline/defs/resources.py`
Schedules: `src/pipeline/defs/schedules/`

## Patterns
Raw assets use the `_make_raw_asset()` factory in `assets/raw_data.py`.
Follow that pattern for any new raw assets.

## Validation
Run `dg check defs` from the project root after any change.
Run `pytest` to verify tests pass.
```

With this file present, the agent reads it at the start of each session and uses your conventions, not the skill's defaults.

## Read before you build

Before adding anything new to an existing project, prompt the agent to explore what's already there:

```text
/dagster-expert Read the existing assets in defs/assets/ and the resource definitions
in defs/resources.py. Describe the patterns and conventions you see before suggesting
any changes.
```

This gives the agent an accurate picture of the codebase and surfaces patterns it should follow. It also gives you a chance to correct any misunderstandings before implementation starts.

For larger projects, you can scope the reading:

```text
/dagster-expert I want to add a new data source. Before writing any code, read the
three most recently modified files in defs/assets/ and describe the pattern I'm
following for raw assets.
```

## Where AI-driven workflows add the most value in brownfield projects

Not all brownfield work benefits equally. The highest-value applications:

**Adding new assets and integrations**: the shape of the work is the same as greenfield. The agent follows the existing factory pattern, scaffolds files in the right location, and adds dependencies. The only difference is that you need to point it at the existing pattern first.

**Applying dignified-python to legacy code**: `dg check defs` doesn't catch style issues; code that works may still be structured poorly. The `/dignified-python` skill will audit existing files and propose improvements -- repetitive asset functions, missing type hints, side effects at import time -- without changing behavior.

**Adding tests**: existing assets often have no tests. The TDD approach from Lesson 6 works on existing assets: write a test that describes the expected behavior, prompt the agent to run it and confirm it passes (or fix it if it doesn't).

**Writing schema and documentation**: the dbt skill can add tests, descriptions, and column documentation to existing dbt models without changing the SQL. Prompt it with a dbt-focused request (e.g. "add `not_null` tests to all id columns in schema.yml") and it activates automatically.

## Where to be careful

**Refactoring core abstractions**: if the project has a custom base class, a non-standard resource pattern, or unusual job structure, the agent may not understand why it exists. Prompt it to explain what it sees before asking it to change anything structural.

**Migrating patterns**: don't prompt the agent to "update all assets to use the new factory pattern" in a single session. The blast radius is large, the agent will read many files, and context degradation (Lesson 7) will affect the later files in the session. Break pattern migrations into one asset at a time, each in its own session, each validated before the next begins.

**Files not covered by your context file**: if a part of the project has conventions your context file doesn't mention, the agent will invent something. Before prompting in an unfamiliar area, read a representative file and add the relevant conventions to your context file.

## The brownfield onboarding prompt

A useful pattern when starting AI-driven work on an unfamiliar existing project: give the agent an explicit onboarding task before any implementation work.

```text
/dagster-expert You're working on an existing Dagster project. Before we add anything new:

1. Read the files in defs/assets/ and defs/resources.py
2. Run `dg check defs` and report what definitions currently exist
3. Describe the patterns you see: how are assets defined, what resources exist,
   what naming conventions are used

Do not make any changes yet. I want to review your understanding before we build.
```

This establishes shared context, surfaces any gaps before they affect the implementation, and gives you a baseline of what currently works. Once the agent can accurately describe the project, subsequent prompts will produce code that fits rather than code that needs correcting.
