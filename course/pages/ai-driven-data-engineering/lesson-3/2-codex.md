---
title: "Lesson 3: Codex"
module: 'ai_driven_data_engineering'
lesson: '3'
---

# Codex

If you’re using **Codex** as your AI coding agent, follow these steps so the Dagster skills are available. Once they’re installed and enabled, you can use prompts like `/dagster-expert` in later lessons.

---

## 1. Install Codex

Install [Codex](https://openai.com/codex/) from the official setup guide for your environment and sign in.

---

## 2. Add the Dagster skills

The `npx` command comes with Node.js. If you don't have it installed, [install Node.js](https://nodejs.org) first.

Install using the `npx skills` command-line:

```bash
npx skills add dagster-io/skills
```

![npx install](/images/ai-driven-data-engineering/lesson-3/npx-install.png)

---

## 3. Ensure the Dagster skills are enabled

In Codex settings or the skill list, confirm that the Dagster-related skills are **enabled**. You want at least:

- `dagster-expert`: for project structure, `dg` CLI, and Dagster patterns
- `dignified-python`: for general Python quality

Once they’re enabled, you can invoke them in your prompts. Type the skill name prefixed with `/` at the start of your message:

```text
/dagster-expert create a new Dagster project called university
```

You’ll use this pattern throughout the rest of the course.

![Codex skill](/images/ai-driven-data-engineering/lesson-3/codex-skill.png)

---

## You’re set

With the Dagster skills installed and enabled, you’re ready for Lesson 4. In later lessons you’ll use the skills so the agent follows Dagster best practices and uses `dg` for scaffolding and validation.
