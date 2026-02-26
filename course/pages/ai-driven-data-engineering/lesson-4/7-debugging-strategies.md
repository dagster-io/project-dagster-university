---
title: "Lesson 4: Debugging strategies"
module: 'ai_driven_data_engineering'
lesson: '4'
---

# Debugging strategies

The debugging page earlier in this lesson showed one specific pattern: a DuckDB path error, fixed in the resource with the skill's help. That pattern—give the error to the agent, use the right skill, fix in the right place—covers many cases. But debugging goes wrong in predictable ways, and knowing how to handle them keeps the workflow moving.

## When debugging is circular

If you've made three different changes and the error hasn't moved, stop and reassess. The problem is probably not where you've been looking.

Signs that debugging has become circular:
- The same error appears after different fixes
- The agent keeps suggesting variations of approaches that haven't worked
- You've lost track of which changes are currently in place and which were reverted

When this happens, the most effective move is to reset. Undo changes back to the last known-good state (the last `dg check defs` passing), then approach the problem with a fresh diagnostic prompt rather than a fix prompt:

```bash
> /dagster-expert I'm getting this error when I run the trending_events asset.
Before suggesting any fixes, explain what could cause it and where to look.
```

Getting the agent to explain the problem first—rather than jumping to a fix—often surfaces the real cause. Fixes to the wrong place don't surface the right cause.

## Rewind when an approach makes things worse

Every change Claude Code makes creates a checkpoint automatically. If the agent takes an approach that introduces new problems—or makes the original problem harder to diagnose—you can revert the conversation and the code together rather than manually undoing each file.

:::note
**In Claude Code:** press `Escape` twice, or type `/rewind`
:::

This restores both the conversation history and the file state to before the last action. The practical use case: the agent made a change that seemed reasonable, the error changed but didn't resolve, and now you're not sure what's current. Rather than trying to piece together what changed, rewind to the last known state and give a better-framed prompt.

Rewind is faster than manual reversion and cleaner than trying to correct the agent mid-flight. It doesn't replace git—it only covers changes made within the current Claude session. Rewind to revert a bad attempt; use `git` to revert across sessions.

## Debugging and session state

Long debugging sessions accumulate noise: stack traces, failed attempts, reverted changes, "try this instead" exchanges. That history doesn't help the current fix—it occupies context that the fix needs.

Once you've solved a debugging problem, consider whether to continue in the same session or start fresh. If the fix is small and the session is short, continue. If the session has accumulated several rounds of wrong approaches, apply the fix in a fresh session: open new, paste the handoff summary plus the error and its solution, make the targeted change, validate, commit. The fix lands cleanly without carrying the debugging noise into the project history.

This isn't a rule—it's a cost-benefit judgment the same way all session management decisions are.
