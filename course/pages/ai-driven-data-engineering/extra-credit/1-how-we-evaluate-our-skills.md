---
title: 'Extra credit: How we evaluate our skills'
module: 'ai_driven_data_engineering'
lesson: 'extra-credit'
---

# How we evaluate our skills

Skills need to be **maintained**. The Dagster library and our recommendations evolve constantly, so we need a way to ensure our skills stay accurate, are actually used by the agent, and produce correct outputs. We built a lightweight evaluation framework to do that. The full story is in the blog post [Evaluating Skills](https://dagster.io/blog/evaluating-agent-skills); here's the summary.

---

## Why we evaluate

Without evaluation, we were mostly hoping that the context in our skills would lead to the right behavior. We wanted to know:

- Is the agent actually using the skill?
- Is it pulling the *right* context for the question?
- Is the resulting code or behavior correct?

So we built a small framework that runs the agent headlessly with a set of prompts and a chosen set of skills, then captures **snapshots**: which skills and tools were used, token usage, and the output. Those snapshots live in version control so we can see how they change as we update the skills.

---

## What we validate

We do more than check "was the skill invoked?" We also validate the *outcome*. For example, after a prompt like "Add a new asset named `dwh_asset`," we:

- Assert that the expected skill (e.g. `dagster-expert`) was used
- Run `dg list defs` and confirm the new asset appears and is valid
- Optionally check metadata and structure

That gives us much higher confidence that the skills are not only referenced but actually driving correct, usable results.

---

## Lessons we've learned

From iterating on the skills and their evaluations, a few themes stand out:

- **Less is more** — Terse, focused skills tend to perform better than long, document-dump-style content. Our first pass was to turn existing docs into skills; the result was too verbose and sometimes inconsistent. Trimming and structuring for the agent improved both behavior and token use.

- **Decision trees** — At the top level of each skill we define a simple decision tree: map phrases or intents (e.g. "schedule this to run daily", "trigger when file arrives") to a *subset* of references. That way the agent only loads what's needed for the task instead of the whole skill.

- **Purpose-built CLIs** — There's no substitute for a good CLI. We use `dg` for scaffolding, checking definitions, and launching runs. The skills direct the agent to these commands instead of having it infer file layout or API usage, which makes behavior more deterministic and easier to evaluate.

- **Feedback loops** — The narrative summary of what the agent did (which tools it called, in what order) lets us quickly see if behavior matches expectations. We can also feed that summary back into an agent to refine the skill's context and instructions, then re-run evaluations to confirm improvements.

---

## Why this matters for you

Evaluations remove guesswork. We can measure whether our skills are helping, spot regressions when we change them, and iterate with clear feedback. That's how we keep the Dagster skills useful as the product and our best practices evolve.

For implementation details, example snapshots, and code, see the [Evaluating Skills](https://dagster.io/blog/evaluating-agent-skills) blog post and the [dagster-io/skills](https://github.com/dagster-io/skills) repository (including the `dagster-skills-evals` directory).
