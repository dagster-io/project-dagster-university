---
title: "Lesson 6: Our patterns"
module: 'ai_driven_data_engineering'
lesson: '6'
---

# Our patterns

The dignified-python skill encodes a set of Python best practices and philosophies we use at Dagster. The rules cover types, exceptions, API design, naming, and structure—things that make code easier to read, maintain, and reason about. They’re not Dagster-specific; you can apply them to any Python project.

---

## Where to see the patterns

The full set of patterns lives in the Dagster Skills repository. You can read the core content here:

- **[dignified-python-core](https://github.com/dagster-io/skills/blob/main/skills/dignified-python/skills/dignified-python/dignified-python-core.md)** — The main skill document that describes the rules and gives examples.

For a shorter, narrative overview aimed at improving LLM-generated code, see the blog post:

- **[Dignified Python: 10 rules to improve your LLM agents](https://dagster.io/blog/dignified-python-10-rules-to-improve-your-llm-agents)** — Ten concrete rules (e.g. avoid side effects at import time, prefer small functions, use type hints, handle errors explicitly) with rationale and examples.

---

## What kind of things it covers

Typical themes in dignified-python include:

- **Import-time behavior** — Avoid doing work (e.g. creating directories, opening connections) at module import; do it when functions are called or when definitions are loaded.
- **Repetition** — Replace repeated logic with helpers or factories (e.g. `_make_raw_asset()` instead of three nearly identical asset functions).
- **Types** — Use type hints for function arguments and return values so the code is easier to understand and tool.
- **Exceptions** — Handle errors explicitly; don’t swallow or ignore them.
- **APIs and naming** — Prefer clear, consistent names and small, focused functions.

When you invoke the `/dignified-python` skill and point the agent at your code, it uses these patterns to suggest improvements. Next we’ll run it on the project we’ve built so far.
