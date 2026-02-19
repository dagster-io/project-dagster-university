---
title: "Lesson 3: Overview of AI tools in the Dagster ecosystem"
module: 'ai_driven_data_engineering'
lesson: '3'
---

# Overview of AI tools in the Dagster ecosystem

Dagster provides a set of tools and patterns to support AI-driven development. Together they help you scaffold projects, stay within best practices, and work effectively with coding agents—without drowning the model in context or letting it drift off-spec.

This lesson gives you a high-level map of what’s in the ecosystem and how the pieces fit together.

---

## What we'll cover

- **What is an MCP server?** — A short explanation of the Model Context Protocol and what an MCP server does, so the CLI-vs-MCP discussion makes sense.

- **The `dg` CLI** — An opinionated CLI for scaffolding, checking, and running Dagster projects. We built it before AI workflows took off; it’s now a core way agents interact with your project in a deterministic way.

- **CLI vs MCPs** — Why we lean on a quality CLI instead of an MCP server for most workflows: less surface area, more predictable behavior for LLMs.

- **Dagster Skills** — A maintained collection of AI skills (Anthropic-style, now usable across coding agents) that give your assistant the right context for Dagster and our integrations. We’ll list the main skills and point to where we go deeper.

- **How we evaluate our skills** — Skills need to stay accurate as Dagster evolves. We’ll summarize how we evaluate and maintain them, with a link to the full post.

Once you have this overview, you’ll be ready to use `dg`, choose the right skills, and understand how we keep them reliable.
