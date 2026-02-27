---
title: "Lesson 2: What is an MCP server?"
module: 'ai_driven_data_engineering'
lesson: '2'
---

# What is an MCP server?

One way to give AI assistants richer context is through MCP. MCP stands for Model Context Protocol—an open protocol that allows AI assistants (e.g., Claude, Cursor) to communicate with external tools and data sources through a standard interface.

## What an MCP server does

An MCP server provides structured context and capabilities to an AI agent. It typically exposes:

- **Tools**: Actions the model can invoke (e.g., “run this query” or “fetch that resource”). Each tool has a name, description, and parameters. The server executes the action and returns the result.
- **Resources**: Data the model can read (e.g., file contents, API responses, database schemas).
- **Prompts**: Predefined prompt templates the client can call.

An AI agent—whether it’s an IDE, chatbot, or agent framework—connects to one or more MCP servers. When you ask it to perform a task, it can call tools and read resources from those servers instead of relying solely on the text in the chat.

## Why MCP got attention

MCP was proposed as a universal way for AI assistants to plug into your stack—databases, APIs, internal tools, and documentation. In principle, a single “Dagster” MCP server could provide consistent tools and context to any MCP-compatible client.

That promise of interoperability is why many teams, including ours, experimented with MCP servers early on.

In the next section, we’ll cover the `dg` and the other Dagster CLIs. After that, we’ll explain why we’ve leaned toward a CLI rather than an MCP server for our core AI-driven workflows—and where MCP can still be useful.
