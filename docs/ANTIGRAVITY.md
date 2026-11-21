# Antigravity Integration

[Google Antigravity](https://antigravity.google/) reads `AGENTS.md` directly, so most of
EMW works there with no adapter at all. This page covers what to copy, what differs from
the other integrations, and what has not been verified.

## What you copy

| Copy | Why |
|---|---|
| `.emw/` | The rules, prompts, templates, tracks and tools. Agent-independent |
| `AGENTS.md` | The contract. Antigravity loads it automatically on every turn |
| `.agents/skills/` | The ten EMW commands and three skills, as Antigravity skills |

No adapter file is needed. `AGENTS.md` **is** the adapter — the same file Codex and
OpenCode use.

## How Antigravity finds them

Per the [rules documentation](https://antigravity.google/docs/rules/), Antigravity reads
`AGENTS.md`, `GEMINI.md` and `.agents/rules/*.md` from the workspace folder and any
parent folder up to the repository root. `AGENTS.md` needs no frontmatter and is treated
as `always_on`, meaning its full content goes into the system prompt on every turn.

Two consequences worth knowing:

- **Rules are cumulative, not replacement-based.** If you copied `GEMINI.md` as well —
  it is the Gemini CLI adapter and points at the same files — both load. That is
  harmless but redundant. For Antigravity alone, `AGENTS.md` is enough.
- **Rules are not read from subfolders.** `AGENTS.md` must sit at the workspace root or
  a parent, not in a subdirectory of the project.

## Size

Antigravity truncates any single rule file over 24,000 bytes. EMW's `AGENTS.md` is about
9,000 bytes, well inside that. All always-on rules also share a 20,000-token budget, and
when it is exceeded the largest files are demoted from inline text to pointers. If you
merge EMW's `AGENTS.md` into a large existing one, keep an eye on the combined size.

## The commands

The ten EMW commands live in `.agents/skills/<name>/SKILL.md`, which is where Antigravity
looks for workspace skills. Each folder holds one file with a `description` in its
frontmatter. Invoke them by typing `/emw-track`, `/emw-practice` and so on, the same
names Claude Code and OpenCode use.

Antigravity also surfaces skills on its own: the agent sees every skill's name and
description each turn and may apply one without being asked, which is how the three
background skills — `emw-workflow`, `emw-knowledge`, `emw-mastery` — are meant to work.

**These files mirror `.claude/commands/` and `.claude/skills/`.** They are adapters with
no policy of their own; the canonical instructions are the prompts in `.emw/prompts/`.
Change a command in one place and change it in the others.

`emw_check` holds them to each other, so drift is an error rather than something to
remember: every integration must offer the same set of commands, their descriptions must
match, and each copy must route to the same `.emw/prompts/` file. `name` is the one field
that may differ, because OpenCode uses readable names where the others use slugs. The
Antigravity bodies are exempt from the word-for-word comparison, since they are
deliberately reworded for the missing `$ARGUMENTS` substitution.

### Arguments

One difference from the other integrations. Claude Code and OpenCode substitute
`$ARGUMENTS` into a command; Antigravity's skills documentation does not describe such a
substitution, so the `.agents/` copies do not rely on it. They refer to "the concept the
developer named in this request" instead, which reads correctly whether or not anything
is substituted.

In practice this means `/emw-track start php` should still work — the agent sees both the
skill and your message — but it is the one part of this integration most likely to behave
differently, and it is worth checking on your first run.

## Workflows

Antigravity also has `.agents/workflows/`, which are invoked with a slash by name and
would be a closer match to Claude Code's commands. EMW does not use them: the
[documentation](https://antigravity.google/docs/ide/workflows/) says workflows are
deprecated and a replacement is coming. Skills are the stable target.

## Not verified

EMW has not been run inside Antigravity. The integration follows the documented
behaviour — file locations, loading rules, size limits, invocation — but nobody has sat
in the IDE and driven a stage of a learning track with it.

If you are the first, the things most worth reporting back are whether `/emw-*`
invocation passes your arguments through, whether the agent honours the Mode 1 coaching
rules without the explicit refusal that Claude Code's adapter carries, and whether
`AGENTS.md` survives the token budget alongside any rules you already had.
