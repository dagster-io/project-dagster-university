---
title: "Lesson 3: Claude Code"
module: 'ai_driven_data_engineering'
lesson: '3'
---

# Claude Code

If you’re using **Claude Code** as your AI coding agent, follow these steps so the Dagster skills are available. Once they’re installed and enabled, you can use prompts like `/dagster-expert` in later lessons.

---

## 1. Install Claude Code

Install and sign in to [Claude Code](https://code.claude.com/docs/en/setup) from the setup guide.

---

## 2. Install the Dagster skill

In Claude Code, add the Dagster skills from the plugin marketplace:

```text
/plugin marketplace add dagster-io/skills
```

![Claude marketplace](/images/ai-driven-data-engineering/lesson-3/claude-marketplace.png)

This installs the Dagster skill pack (including `dagster-expert` and `dignified-python`) so the agent has the right context for building with Dagster.

---

## 3. Ensure the Dagster skills are enabled

Open the plugin list and confirm the Dagster skills are enabled:

```text
/plugin
```

Switch to the **Installed** tab and verify that the Dagster skills show as enabled. You should see something like:

- **dagster-expert**: enabled
- **dignified-python**: enabled

If any are disabled, enable them so the agent can use Dagster best practices and the `dg` CLI when you invoke the skill in your prompts.

![Claude plugin](/images/ai-driven-data-engineering/lesson-3/claude-plugin.png)

---

## How to invoke skills

In Claude Code, skills are invoked as slash commands. Type the skill name prefixed with `/` at the start of your prompt:

```text
/dagster-expert create a new Dagster project called university
```

Claude Code loads that skill’s context before responding. You’ll use this pattern throughout the rest of the course.

---

## You’re set

With the Dagster skills installed and enabled, you’re ready for Lesson 4. In later lessons you’ll use the skills so the agent follows Dagster best practices and uses `dg` for scaffolding and validation.
