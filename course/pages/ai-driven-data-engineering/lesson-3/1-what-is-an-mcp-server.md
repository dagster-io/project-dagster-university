---
title: "Lesson 3: What is an MCP server?"
module: 'ai_driven_data_engineering'
lesson: '3'
---

# What is an MCP server?

MCP stands for Model Context Protocol. It’s an open protocol that lets AI assistants (e.g. Claude, Cursor) talk to external tools and data sources through a standard interface.

---

## What an MCP server does

An **MCP server** is a process that speaks the MCP protocol. It exposes to the model:

- **Tools** — Actions the model can invoke (e.g. “run this query”, “fetch that resource”). Each tool has a name, description, and parameters, and the server runs the action and returns a result.
- **Resources** — Data or context the model can read (e.g. file contents, API responses, database schema).
- **Prompts** (in some setups) — Predefined prompt templates the client can call.

The AI client (IDE, chatbot, or agent framework) connects to one or more MCP servers. When you ask the model to do something, it can call the server’s tools and read its resources instead of only using the context you pasted into the chat.

---

## Why MCP got attention

MCP was proposed as a common way for any AI assistant to plug into your stack: databases, APIs, internal tools, docs. In theory, a single MCP server for “Dagster” could give every MCP-capable client the same tools and context. That’s why many teams, including us, tried building MCP servers early on.

In the next section we’ll cover the **`dg`** CLI, and after that we’ll explain why we’ve leaned on a CLI rather than an MCP server for our main AI-driven workflows—and when MCP can still be useful.
