# GitHub Copilot Instructions

This repository uses Engineering Mastery Workflow (EMW).

Follow root [AGENTS.md](../AGENTS.md). At session start, read [.emw/prompts/README.md](../.emw/prompts/README.md) and [.emw/prompts/00-session-start.md](../.emw/prompts/00-session-start.md). Automatically read the task-specific prompt when its trigger occurs, provided the active Copilot surface has repository instruction and file access.

For consuming projects, use Prompt 01 when onboarding records are missing or stale. Before meaningful work, retrieve relevant shared knowledge from [.emw/knowledge/](../.emw/knowledge/) and project knowledge from `.project-knowledge/`. Capture durable verified project lessons; never publish project knowledge to shared EMW without sanitization and human approval.

Use the six-stage lifecycle and select an appropriate collaboration mode. Keep engineering delivery separate from developer mastery. Do not infer mastery from AI-generated code or claim checks passed unless they were actually run. Treat authorization, multi-tenancy, payments, secrets, privacy, and destructive operations as high risk requiring human review.

See [Using EMW with Any Agent](../docs/USING-WITH-ANY-AGENT.md).
