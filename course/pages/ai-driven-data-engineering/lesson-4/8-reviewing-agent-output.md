---
title: "Lesson 4: Reviewing agent output"
module: 'ai_driven_data_engineering'
lesson: '4'
---

# Reviewing agent output

`dg check defs` confirms that definitions load without errors. It doesn't confirm that the code is correct, that it follows project conventions, or that the agent only changed what you asked it to change. That review is your responsibility, and it's a consistent part of the workflow—not an occasional sanity check.

---

## What `dg check defs` does and doesn't catch

`dg check defs` validates the definitions layer: assets are correctly decorated, resources are registered, schedules reference valid jobs. If a definition fails to load, it reports an error with a traceback.

What it doesn't check:
- Whether the logic inside an asset function is correct
- Whether the code follows the project's conventions (the factory pattern, the DuckDB path structure)
- Whether the agent changed files you didn't intend it to change
- Whether values are hardcoded when they should come from resources or env vars

A pass from `dg check defs` means "this loads." It doesn't mean "this is what you asked for."

---

## Use git diff as the review step

Before accepting agent output, look at what changed. `git diff` is the clearest way to do this:

```bash
git diff
```

The diff tells you two things:

**Scope** — which files were modified. If you asked for a change to `assets/trending_events.py` and the diff shows changes to `resources.py` and `schedules/daily_raw.py` as well, something unexpected happened. It may be intentional and correct—or it may be the agent "helpfully" tidying things it shouldn't have touched.

**Content** — what specifically changed within each file. Read the removed lines alongside the added lines. This is where convention violations are visible: if the agent wrote a new asset directly instead of using `_make_raw_asset()`, the diff shows it. If it hardcoded a DuckDB path instead of using the path constant, the diff shows it.

The review doesn't need to be exhaustive. For small changes, a quick scan of the diff is enough. For larger changes across multiple files, be more deliberate.

---

## Patterns worth watching for

**Convention violations.** If the project has established a pattern—a factory function, a naming scheme, a specific import style—new code generated mid-session may drift from it, especially in longer sessions. Check that new code follows the same patterns as what already exists.

**Unexpected file changes.** The agent sometimes fixes adjacent issues it notices while working on the main task. Those fixes may be correct, but you didn't ask for them, and they add scope you haven't validated separately. Decide whether to keep them or revert them.

**New files when editing an existing one would suffice.** If you asked for a small addition to an existing asset file and the agent created a new file alongside it, that's worth questioning. New files add indirection. The agent tends to default to "create new" when "edit existing" is simpler.

**Hardcoded values.** Paths, bucket names, API endpoints—the agent will sometimes write these literally when they should come from an env var or a constant. This is easy to miss in a large diff.

**Unnecessary abstraction.** The agent occasionally introduces a helper or wrapper for a one-time operation. If something is used exactly once, the abstraction usually adds complexity without benefit.

---

## Requesting targeted revisions

When you see a problem in the diff, describe it precisely rather than asking for a redo:

**Broad:**
```
This isn't right, try again
```

**Targeted:**
```
The change to resources.py is wrong—revert that file to what it was before.
Keep the changes to assets/trending_events.py.
```

Or, for a convention issue:

```
The new asset defines the function directly. It should use _make_raw_asset() like the
other three raw assets. Only change the asset definition—don't touch the import block.
```

Targeted revisions keep the session clean. They leave correct changes in place and fix only what's wrong, without asking the agent to reconsider decisions that were right the first time.
