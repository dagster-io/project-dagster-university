---
title: "Lesson 2: Claude Code"
module: 'ai_driven_data_engineering'
lesson: '2'
---

# Claude Code

If you’re using **Claude Code** as your AI coding agent, follow these steps so the Dagster skills are available. Once they’re installed and enabled, you can use prompts like `/dagster-expert` or `/dagster-integrations` in later lessons.

---

## 1. Install Claude Code

Install and sign in to Claude Code from the setup guide:

[Claude Code setup](https://code.claude.com/docs/en/setup)

---

## 2. Install the Dagster skill

In Claude Code, add the Dagster skills from the plugin marketplace:

```
/plugin marketplace add dagster-io/skills
```

This installs the Dagster skill pack (including `dagster-expert`, `dagster-integrations`, and `dignified-python`) so the agent has the right context for building with Dagster.

---

## 3. Ensure the Dagster skills are enabled

Open the plugin list and confirm the Dagster skills are enabled:

```
/plugin
```

Switch to the **Installed** tab and verify that the Dagster skills show as enabled. You should see something like:

- **dagster-expert** — ✔ enabled  
- **dagster-integrations** — ✔ enabled  
- **dignified-python** — ✔ enabled  

If any are disabled, enable them so the agent can use Dagster best practices and the `dg` CLI when you invoke the skill in your prompts.

---

## You’re set

Once the Dagster skills are installed and enabled, you can proceed to Lesson 3. In later lessons you’ll use prompts such as `/dagster-expert create a new Dagster project called university` to get behavior that follows our recommended project layout and tooling.
