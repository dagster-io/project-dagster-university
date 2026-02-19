---
title: "Lesson 6: Dignified Python vs linters"
module: 'ai_driven_data_engineering'
lesson: '6'
---

# Dignified Python vs linters

How is **dignified-python** different from a linter like **Ruff**? And can you use both? Yes—internally we use both, for different reasons.

---

## How they differ

**Ruff** (and linters like it) is **deterministic**. Given the same code and config, it always reports the same issues. It runs quickly, fits into CLI and CI pipelines, and catches a well-defined set of problems: style (e.g. line length, quotes), common bugs (unused imports, undefined names), and rule-based patterns. It doesn’t “understand” higher-level design or narrative best practices; it applies fixed rules.

**Dignified-python** is an **AI skill**. The agent reads the skill’s rules and your code, then suggests changes based on those patterns. It can address structure (e.g. “move this side effect inside a function”), repetition (“factor these three functions into one helper”), and design choices that are hard to encode as linter rules. The output can vary slightly between runs or agents, and it requires an AI assistant in the loop.

So: **Ruff** = deterministic, fast, great for pipelines and consistent style. **Dignified-python** = broader, design- and structure-oriented, used with an agent to improve code quality beyond what a linter checks.

---

## Using them together

We use both:

- **Ruff** — Run in CI and as part of the development workflow (e.g. `ruff check .`, `ruff format .`). Because it’s deterministic, it’s safe to run in CLI pipelines and to fail builds when rules are violated. It catches a different set of issues (formatting, many static bugs, import order) quickly and reliably.

- **Dignified-python** — Invoke when you want the agent to review or refactor code against our Python best practices. Use it for structural improvements, reducing repetition, and import-time vs runtime behavior. It doesn’t replace Ruff; it complements it by addressing the kinds of issues linters don’t typically cover.

**Workflow:** Run Ruff (and fix what it reports) so the codebase stays consistent and passes CI. Use the dignified-python skill when you’re editing or reviewing code with an agent and want suggestions that go beyond what the linter can do. Together they keep the code both lint-clean and aligned with our broader Python standards.
