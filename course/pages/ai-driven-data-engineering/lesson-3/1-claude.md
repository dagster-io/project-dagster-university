---
title: "Lesson 3: Claude Code"
module: 'ai_driven_data_engineering'
lesson: '3'
---

# Claude Code

If you’re using **Claude Code** as your AI coding agent, follow these steps so the Dagster skills are available. Once they’re installed and enabled, you can use prompts like `/dagster-expert` in later lessons.

---

## 1. Install Claude Code

Install and sign in to [Claude Code](https://docs.anthropic.com/en/docs/claude-code/setup) using the setup guide.

---

## 2. Install the Dagster skill

In Claude Code, add the Dagster skills from the plugin marketplace:

```text
/plugin marketplace add dagster-io/skills
```

![Claude marketplace](/images/ai-driven-data-engineering/lesson-3/claude-marketplace.png)

Then install both Dagster skills:

```text
/plugin install dagster-expert@dagster-skills
```

```text
/plugin install dignified-python@dagster-skills
```

---

## 3. Reload plugins

After installing, reload the plugin registry so Claude Code picks up the new skills:

```text
/reload-plugins
```

---

## 4. Ensure the Dagster skills are enabled

Open the plugin list and confirm the Dagster skills are enabled:

```text
/plugin
```

Switch to the **Installed** tab and verify that the Dagster skills show as enabled. You should see something like:

- **dagster-expert**: enabled
- **dignified-python**: enabled

If a skill is missing from the list, install it individually:

```text
/plugin install dagster-expert@dagster-skills
```

```text
/plugin install dignified-python@dagster-skills
```

Then run `/reload-plugins` again before continuing.

If a skill is listed but disabled, enable it so the agent can use Dagster best practices and the `dg` CLI when you invoke the skill in your prompts.

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
