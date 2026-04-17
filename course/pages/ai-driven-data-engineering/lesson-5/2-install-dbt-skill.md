---
title: "Lesson 5: Installing the dbt skill"
module: 'ai_driven_data_engineering'
lesson: '5'
---

# Installing the dbt skill

All of this can be accomplished using only the `dagster-expert` skill, it knows a good deal about dbt, in particular how dbt relates to Dagster. But the dbt skill gives the agent deeper context about dbt such as model patterns, schema YAML, `ref()` and `source()` usage, dbt commands.

With both skills, the agent can know about `DbtProjectComponent` for Dagster and dbt specifics when necessary. This will make more sense when we discuss skill chaining.

Installation is the same regardless of which AI coding agent you use and should look familiar from when we discussed [installing the Dagster skill](/ai-driven-data-engineering/lesson-3/0-overview).

---

## Claude Code

In Claude Code, add the dbt skills from the plugin marketplace and then install the plugin:

```text
/plugin marketplace add dbt-labs/dbt-agent-skills
```

```text
/plugin install dbt@dbt-agent-marketplace
```

Then reload the plugin registry:

```text
/reload-plugins
```

Once installed, confirm it's enabled:

```text
/plugin
```

Switch to the **Installed** tab and verify that the dbt skills show as enabled. You should see entries like:

- **dbt:using-dbt-for-analytics-engineering**: enabled
- **dbt:running-dbt-commands**: enabled

---

## Codex, Cursor, Copilot 

Install using the `npx skills` command:

```bash
npx skills add dbt-labs/dbt-agent-skills
```

Confirm the dbt skills appear in your skill list and are enabled. You want at least `dbt:using-dbt-for-analytics-engineering` available.

---

## You're set

Once the dbt skill is installed, it activates automatically when your prompt is about dbt work -- writing models, updating `schema.yml`, running dbt commands. You don't invoke it with a slash command; it loads based on what you ask. In the next section you'll see it activate as you scaffold the dbt project alongside the Dagster integration.
