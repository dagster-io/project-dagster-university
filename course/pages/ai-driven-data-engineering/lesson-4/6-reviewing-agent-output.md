---
title: "Lesson 4: Reviewing agent output"
module: 'ai_driven_data_engineering'
lesson: '4'
---

## What `dg check defs` does and doesn't catch

`dg check defs` validates the definitions layer in the Dagster project: assets are correctly decorated, resources are registered, schedules reference valid jobs. If a definition fails to load, it reports an error with a traceback. Having a quick feedback loop is very handy but doesn't catch everything.

`dg check defs` doesn't check:
- Whether the logic inside an asset function is correct
- Whether the code follows the project's conventions (the factory pattern, the DuckDB path structure)
- Whether the agent changed files you didn't intend it to change
- Whether values are hardcoded when they should come from resources or env vars

## Having agents execute and troubleshoot

When using Dagster skills, the agent will use `dg check defs` quite often. That is because the operation is so quick and can help the agent ensure everything looks good before moving onto more expensive steps.

![Agent flow 1](/images/ai-driven-data-engineering/lesson-4/agent-flow-1.png)

After you have code that passes `dg check defs`, you can have the agent execute the newly created code by instructing it to execute.

```bash
> /dagster-expert ensure the assets run correctly
```

Because the agent will launch everything from `dg`, it will have access to all of the logs and output of the execution. This way it will be able to tell if code can execute successfully.

![Agent flow 2](/images/ai-driven-data-engineering/lesson-4/agent-flow-2.png)

If there is an error while executing the code, it can take the same iterative approach of editing code, ensuring `dg check defs` and executing the code until the run is successful.

![Agent flow 3](/images/ai-driven-data-engineering/lesson-4/agent-flow-3.png)

