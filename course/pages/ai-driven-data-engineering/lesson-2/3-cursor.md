---
title: "Lesson 2: Cursor"
module: 'ai_driven_data_engineering'
lesson: '2'
---

# Cursor

If you’re using **Cursor** as your AI coding agent, follow these steps so the Dagster skills are available. Once they’re installed and enabled, you can use prompts like `/dagster-expert` or `/dagster-integrations` in later lessons.

---

## 1. Install Cursor

Install Cursor from [cursor.com](https://cursor.com) and sign in.

---

## 2. Add the Dagster skills

Install using the `npx skills` command-line:

```
npx skills add dagster-io/skills
```

![npx install](/images/ai-driven-data-engineering/lesson-2/npx-install.png)

---

## 3. Ensure the Dagster skills are enabled

Confirm that the Dagster skills are **enabled**. You want at least:

- `dagster-expert` — for project structure, `dg` CLI, and Dagster patterns  
- `dagster-integrations` — for adding and configuring integrations (e.g. dbt, Sling)  
- `dignified-python` — for Python best practices  

Skills are often invoked by typing `/` in the chat and selecting the skill, or by including the skill name in your prompt.

![Cursor skill](/images/ai-driven-data-engineering/lesson-2/cursor-skill.png)

---

## You’re set

Once the Dagster skills are installed and enabled, you’re ready for Lesson 3. In later lessons you’ll use prompts that invoke these skills so the agent follows Dagster best practices and uses `dg` for scaffolding and validation.
