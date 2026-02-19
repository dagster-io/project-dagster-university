---
title: "Lesson 1: AI Driven vs AI Pipelines"
module: 'ai_driven_data_engineering'
lesson: '1'
---

# AI Driven vs AI Pipelines

It's important to distinguish between two different ways "AI" and "data" come together—**AI pipelines** and **AI-driven development**. This course focuses on the latter.

---

## AI Pipelines

**AI pipelines** are workflows that support AI infrastructure and applications. Examples include:

- **RAG (Retrieval-Augmented Generation)** pipelines that ingest documents, build embeddings, and serve them to LLMs
- **Model training and deployment** pipelines that prepare data, train models, and ship them to production
- **Feature stores** and data pipelines that feed ML models

Dagster fully supports these workflows. You can orchestrate RAG, training jobs, and other AI/ML pipelines with assets, schedules, and resources. If you're building that kind of system, Dagster is a great fit—but that's not what this course is about.

---

## AI-Driven Development

**AI-driven (data) engineering** is about using AI to *build* your data platform and Dagster applications—faster, more safely, and in line with best practices.

In this model, AI assists you as a developer: it can help you write assets, define dependencies, set up resources, and debug runs. The goal is to use AI so you can develop Dagster code more quickly, easily, and safely, without having to look up every API or pattern by hand.

---

## Why this course focuses on AI-driven workflows

This course is focused on **AI-driven workflows**: how you use AI tools to develop and operate Dagster applications. We'll cover the AI tooling Dagster provides and the patterns that help you write better code and get to production sooner. If you're interested in building AI/ML pipelines *inside* Dagster, you can combine those with what you learn here—but here we're optimizing for *how you build with Dagster*, not for building RAG or model pipelines themselves.
