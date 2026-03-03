---
title: "Lesson 6: Cleaning up our code"
module: 'ai_driven_data_engineering'
lesson: '6'
---

# Cleaning up our code

Let’s apply the **dignified-python** skill to the code we’ve written in this course. Prompts for this skill can be general or very specific. We’ll start with a general question so the agent reviews the codebase against the dignified-python rules.

## Ask the skill to review

Point the agent at your project (e.g. the raw assets and resources) and ask:

```text
/dignified-python Review defs/assets/raw_data.py and defs/resources.py. Does this follow Python best practices?
```

The agent loads the dignified-python context and analyzes the code. It may report several issues and suggest concrete changes.

## Example improvements it finds

Two typical improvements the skill might suggest:

**1. Move `mkdir()` inside `resources()`**

In `resources.py`, the database path’s parent directory might be created at import time (e.g. `_DB_PATH.parent.mkdir(parents=True, exist_ok=True)` at module level). That means the directory is created as soon as the module is imported, which can be surprising and makes the module harder to test or load in contexts where you don’t want side effects yet.

The skill suggests moving the `mkdir()` call inside the function that builds the `Definitions` (e.g. inside `resources()`), so the directory is created only when that function is called, i.e. when definitions are actually being loaded, not on every import.

**2. Replace repeated asset logic with a helper**

The three raw assets (`raw_customers`, `raw_orders`, `raw_payments`) might be defined as three almost identical functions that differ only by URL, table name, and asset name. That repetition violates the “don’t repeat yourself” idea and makes the file longer and harder to change.

The skill suggests introducing a single helper (e.g. `_make_raw_asset()`) that takes the URL, table name, and asset name as arguments and returns an asset. The three assets are still registered under the same names and group as before; they’re just defined via the helper so there’s no duplicated logic.

## Result

After applying the suggested changes, the codebase is cleaner: no import-time side effects and less duplication. You can run `dg check defs` to confirm everything still loads, and the behavior of your pipeline is unchanged. The dignified-python skill is most useful when you want the agent to improve style and structure without changing what the code does.
