---
title: "Lesson 9: Working with an existing project"
module: 'ai_driven_data_engineering'
lesson: '9'
---

# Working with an existing project

Everything in this course started from a blank directory. Most real-world use cases don't. You likely have an existing Dagster project—possibly with the older flat layout from Lesson 4's "without skill" example, possibly a project that predates `dg` entirely. The skill-driven workflow applies in all of these cases, but it requires a bit more deliberate setup.

---

## Orient the agent before asking for changes

When you open a session against a codebase the agent hasn't seen, your first message shouldn't be a change request. It should be an orientation prompt:

```
/dagster-expert Read the project structure and describe what each file does,
what assets are defined, and what conventions the existing code follows.
```

This does two things: it loads the codebase into the session context before any changes are made, and it surfaces the conventions already in use so later prompts can ask the agent to follow them.

Read the agent's description. If it describes the existing patterns accurately—the resource setup, the asset naming, the dependency structure—you can rely on it to follow those patterns in subsequent prompts. If it misses something important, correct it now:

```
The assets are all defined using a _make_raw_asset() factory in raw_data.py.
Any new raw assets should follow that pattern, not define functions directly.
```

Getting the agent oriented before the first change request is cheaper than correcting drift after multiple changes.

---

## Run `dg check defs` before making any changes

Establish a baseline. Run `dg check defs` on the existing project before asking the agent for anything:

```bash
dg check defs
```

If it passes, you know the starting state. If it fails—and it might, if the project predates `dg`'s stricter validation or has accumulated definition errors—that's useful information too. Fix the pre-existing issues before layering new changes on top of them.

This also gives you a clear before/after comparison: if `dg check defs` passes before your change and fails after it, the change introduced the problem.

---

## Protect what works

When you ask for additions, be explicit about what should not change:

```
/dagster-expert Add a new asset called raw_events that loads from [URL] into DuckDB.
Don't change any existing asset definitions or the resource config.
```

Without these constraints, the agent may decide to "improve" adjacent code while adding the new feature. Those improvements may be correct by `dignified-python` standards, but they add unreviewed scope to a change you intended to be minimal. Add scope deliberately, not as a side effect.

---

## Reorganizing toward the `defs/` layout

If your existing project uses the older flat layout (`assets.py`, `definitions.py` at the top level), the agent will often suggest or attempt to reorganize it toward the `defs/` structure—sometimes unprompted, sometimes explicitly.

That reorganization is usually the right long-term move. But it's a significant change and shouldn't happen as a side effect of something else.

If you want to migrate, do it as a dedicated, deliberate task:

```
/dagster-expert Reorganize this project to use the defs/ layout:
assets under defs/assets/, resources in defs/resources.py, and schedules
in defs/schedules.py. Don't change any logic—only move and reorganize.
Run dg check defs after to confirm nothing broke.
```

By framing the reorganization as "move and reorganize, don't change logic," you're asking for a structural change with a clear validation signal (`dg check defs` passing after). You can commit the reorganization as its own commit before adding any new functionality on top.

If you don't want to migrate right now, say so explicitly:

```
Don't reorganize the project layout—work within the existing flat structure.
```

The agent will follow this constraint. The flat layout still works; the `defs/` structure makes things easier as the project grows, but it's not required for the skill-driven workflow to function.

---

## Incremental is safer than all-at-once

The general principle for brownfield work: smaller changes, validated more often.

Every change is a prompt, a `dg check defs` pass, and a commit before the next prompt. That discipline matters more in an existing project than in a greenfield one, because the blast radius of an unexpected change is larger when there's already a working pipeline to break.

When something does break, a short commit history makes it easy to identify which change introduced the problem. When everything is working, a clean commit history makes it easy to hand the project off to someone else—or to your future self opening a new session weeks later.
