---
title: "Lesson 3: GitHub Copilot"
module: 'ai_driven_data_engineering'
lesson: '3'
---

# GitHub Copilot

If you're using **GitHub Copilot** as your AI coding agent, follow these steps so the Dagster skills are available. Once they're installed and enabled, you can use prompts like `/dagster-expert` in later lessons.

---

## 1. Install GitHub Copilot

Install the [GitHub Copilot extension](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot) in VS Code and sign in with your GitHub account. Make sure you also have the [GitHub Copilot Chat extension](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot-chat) installed, which provides the agent interface.

---

## 2. Add the Dagster skills

Install using the `npx skills` command-line:

```bash
npx skills add dagster-io/skills
```

![npx install](/images/ai-driven-data-engineering/lesson-3/npx-install.png)

---

## 3. Ensure the Dagster skills are enabled

In the Copilot Chat panel, confirm that the Dagster skills are **enabled**. You want at least:

- `dagster-expert`: for project structure, `dg` CLI, and Dagster patterns
- `dignified-python`: for Python best practices

Skills are invoked by typing `/` in the Copilot Chat input and selecting the skill, or by including the skill name directly in your prompt.

![GitHub Copilot skill](/images/ai-driven-data-engineering/lesson-3/copilot-skill.png)

---

## You're set

With the Dagster skills installed and enabled, you're ready for Lesson 4. In later lessons you'll use prompts that invoke these skills so the agent follows Dagster best practices and uses `dg` for scaffolding and validation.
