---
title: "Lesson 2: Cursor"
module: 'ai_driven_data_engineering'
lesson: '2'
---

# Cursor

If you’re using **Cursor** as your AI coding agent, you need to add and enable the Dagster skills so the agent has the right context for building with Dagster. Cursor supports skills and plugins; the steps below get the Dagster skills available in your environment.

---

## 1. Install Cursor

Install Cursor from [cursor.com](https://cursor.com) and sign in.

---

## 2. Add the Dagster skills

Cursor can load skills from a few places:

- **Plugins:** If Cursor’s plugin marketplace lists Dagster or Agent Skills, you can install the Dagster skills from there (e.g. search for “Dagster” or “dagster-io/skills”).
- **Skills directory:** You can install skills manually by copying the [Dagster skills](https://github.com/dagster-io/skills) repository (or the skill folders that contain `SKILL.md`) into Cursor’s skills directory. This is often:
  - **Global:** `~/.cursor/skills/`
  - **Project-specific:** `.cursor/skills/` in your project root  

  Place the skill folders (e.g. `dagster-expert`, `dagster-integrations`, `dignified-python`) inside that directory so Cursor can discover them.
- **CLI (if available):** Some setups support `npx`-based installers that add skills for Cursor; check the [Dagster skills README](https://github.com/dagster-io/skills) for current instructions.

---

## 3. Ensure the Dagster skills are enabled

In Cursor’s settings (e.g. **Settings → Features → Skills** or **Plugins**), confirm that the Dagster skills are **enabled**. You want at least:

- **dagster-expert** — for project structure, `dg` CLI, and Dagster patterns  
- **dagster-integrations** — for adding and configuring integrations (e.g. dbt, Sling)  
- **dignified-python** (optional) — for Python best practices  

Skills are often invoked by typing `/` in the chat and selecting the skill, or by including the skill name in your prompt.

---

## You’re set

Once the Dagster skills are installed and enabled, you’re ready for Lesson 3. In later lessons you’ll use prompts that invoke these skills so the agent follows Dagster best practices and uses `dg` for scaffolding and validation.
