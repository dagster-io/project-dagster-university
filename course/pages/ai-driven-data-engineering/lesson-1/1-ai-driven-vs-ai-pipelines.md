---
title: "Lesson 1: AI Driven vs AI Pipelines"
module: 'ai_driven_data_engineering'
lesson: '1'
---

# AI Driven vs AI Pipelines

It's important to distinguish between two different ways "AI" and "data" come together: **AI pipelines** and **AI-driven development**. This course focuses on the latter.

## AI Pipelines

AI pipelines are workflows that support AI infrastructure and applications. Examples include:

- RAG (Retrieval-Augmented Generation) pipelines that ingest documents, build embeddings, and serve them to LLMs
- Model training and deployment pipelines that prepare data, train models, and ship them to production
- Feature stores and data pipelines that feed ML models

Dagster fully supports these workflows. You can orchestrate RAG, training jobs, and other AI/ML pipelines with assets, schedules, and resources. If you're building that kind of system, Dagster is a great fit but that's not what this course is about.

## AI-Driven Development

AI-driven (data) engineering is about using AI to *build* your data platform and Dagster applications faster, more safely, and in line with best practices.

In this model, AI assists you as a developer: it can help you write assets, define dependencies, set up resources, and debug runs. The goal is to use AI so you can develop Dagster code more quickly, easily, and safely, without having to look up every API or pattern by hand.

## Why this course focuses on AI-driven workflows

This course is focused on **AI-driven workflows**: how you use AI tools to develop and operate Dagster applications. We'll cover the AI tooling Dagster provides and the patterns that help you write better code and get to production sooner. If you're interested in building AI/ML pipelines inside Dagster, you can combine those with what you learn here—but here we're optimizing for how you build with Dagster, not for building RAG or model pipelines themselves.

# Benefits of AI Driven

Data engineering can be overwhelming. There are many concepts to learn, patterns to follow, and details to get right. Dagster is built to be the best tool for building and operating data platforms—and AI-driven workflows help you take advantage of it without having to know everything upfront.

* Ship faster - With the right AI tools and patterns, work that might normally take weeks can move to minutes. You can go from an idea or a prompt to a runnable asset, a new dependency, or a small refactor in a fraction of the time. AI can draft code that follows Dagster conventions, so you spend less time on boilerplate and more on your data and business logic.

* Build with best practices - Dagster has strong opinions about how to structure assets, resources, and jobs. AI tools that are aware of those patterns can suggest and generate code that aligns with Dagster best practices—reducing mistakes and technical debt as you go.

* Lower the learning curve - You don't have to memorize every abstraction before you're productive. Using AI that understands Dagster, you can get features to production quickly and deepen your understanding of concepts (assets, resources, schedules, etc.) as you need them. The goal is to jumpstart your flow and then iterate with confidence.
