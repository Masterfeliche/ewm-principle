# Claude Code Instructions

This repository uses Engineering Mastery Workflow (EMW).

Before meaningful work, read and follow:
1. [Root AGENTS.md](AGENTS.md).
2. [.emw/prompts/README.md](.emw/prompts/README.md) and [.emw/prompts/00-session-start.md](.emw/prompts/00-session-start.md).
3. The task-specific prompt selected by the routing table.
4. Relevant policies in [.emw/core/](.emw/core/).

Automatically run the onboarding prompt when a consuming project's onboarding records are absent or stale. Retrieve relevant shared and project knowledge before meaningful work. Capture verified, durable lessons in project knowledge; shared contributions require sanitization and human approval.

## Slash commands and skills
This repository ships Claude Code commands in `.claude/commands/` and skills in `.claude/skills/`. They route to the canonical `.emw/prompts/` files and add no policy of their own.
- `/emw-onboard`, `/emw-feature`, `/emw-learn`, `/emw-debug`, `/emw-review`, `/emw-weekly`, `/emw-capture`, `/emw-practice`, `/emw-track`, `/emw-recall`
- Skills: `emw-workflow`, `emw-knowledge`, `emw-mastery` (loaded automatically when relevant)

## Validate records
After changing knowledge entries or project ledgers, run `python .emw/tools/emw_check.py` and fix every error before reporting the work done. The same check lints every agent adapter's frontmatter and holds the integrations' copies to each other, so edit a command in one integration and edit it in all of them.

Keep engineering delivery and developer mastery separate. Never infer mastery from AI-generated code or claim checks passed unless they were run. See [Using EMW with Any Agent](https://github.com/Masterfeliche/ewm-principle/blob/main/docs/USING-WITH-ANY-AGENT.md) (the `docs/` directory is not copied into a consuming project).
