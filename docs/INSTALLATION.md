# Installing EMW in a Project

EMW is installed in the repository it governs. Shared framework files and the project's own working records must remain separate.

## Recommended: copy or vendor the framework
1. Copy the framework's `.emw/` directory into the target repository.
2. Copy or merge root `AGENTS.md` into the target root.
3. Add the relevant adapter: `CLAUDE.md`, `GEMINI.md`, `.cursor/rules/emw.mdc`, `.github/copilot-instructions.md`, the OpenCode configuration described in [OpenCode Integration](OPENCODE.md), or the `.agents/skills/` directory described in [Antigravity Integration](ANTIGRAVITY.md). Antigravity and Codex need no adapter file of their own: they read root `AGENTS.md` directly.
4. If the target already has an agent instruction or configuration file, merge the EMW reference into it; never blindly overwrite existing project instructions.
5. Copy `.emw/templates/README-project-state.md` as a guide. The onboarding prompt creates project-owned `.emw-project/` and `.project-knowledge/` records.
6. Commit the framework integration.

## Git remote option
Use this to pull the framework straight from the upstream repository without copying files by hand. Run it from the target project repository.

```bash
git remote add emw https://github.com/Masterfeliche/ewm-principle.git
git fetch emw
git checkout emw/main -- .emw
git commit -m "Add the EMW framework"
```

This copies only the upstream `.emw/` directory into your `.emw/`. Do not use `git subtree add --prefix=.emw emw main`: it places the whole upstream repository inside `.emw/`, so the framework ends up at `.emw/.emw/` and no agent or tool finds it.

Copy or merge the root agent instruction files separately. Keep project records outside `.emw/` so upstream updates cannot overwrite them.

To update the framework later:

```bash
git fetch emw
git rm -r -q .emw
git checkout emw/main -- .emw
git commit -m "Update the EMW framework"
```

The update replaces `.emw/` with the upstream copy, including removing files that upstream deleted. Any change you made inside `.emw/` is lost, so review `git diff --cached` before you commit and keep local additions outside `.emw/`.

If the `emw` remote already exists, do not add it again. If the target already has an `.emw/` directory with local changes, inspect and merge it carefully first; do not overwrite local framework modifications or project data.

## Claude Code
Claude Code reads root `CLAUDE.md`. Also copy `.claude/commands/` and `.claude/skills/` for the `/emw-*` slash commands and EMW skills. If the target already has a `.claude/` directory, add these files alongside its own; do not overwrite existing commands or settings.

## Validate the install
Run `python .emw/tools/emw_check.py` from the repository root (needs `pip install pyyaml`). Run it again after onboarding and after any knowledge or ledger change. To enforce it, add the same command to CI or a pre-commit hook.

## OpenCode
OpenCode natively reads root `AGENTS.md`. To get the richer integration, also merge the framework's `opencode.json`, `.opencode/skills/`, and `.opencode/commands/` into the target project. If the target already has `opencode.json`, merge the `instructions` array instead of replacing its settings. See [OpenCode Integration](OPENCODE.md) for commands, skills, and setup.

## Project-owned locations
A consuming repository should have:

```text
project/
├── AGENTS.md
├── opencode.json                # If using OpenCode; merge existing config
├── .opencode/                   # If using OpenCode
│   ├── skills/
│   └── commands/
├── .emw/                        # Shared framework files, updated from upstream
│   ├── core/
│   ├── prompts/
│   ├── knowledge/
│   └── templates/
├── .emw-project/                # This project's own status and ledgers
│   ├── onboarding-status.yaml
│   ├── project-profile.md
│   ├── delivery-ledger.md
│   └── skill-ledger.yaml
├── .project-knowledge/          # This project's own durable knowledge
│   ├── README.md
│   ├── index.yaml
│   ├── architecture/
│   ├── business-rules/
│   ├── integrations/
│   ├── debugging/
│   └── security/
└── src/
```

## First session and automatic onboarding
1. Open the repository root in an agent that can read its files.
2. Ensure root `AGENTS.md` is loaded. If the agent does not auto-load it, paste the universal bootstrap prompt from `.emw/prompts/00-bootstrap-any-agent.md`.
3. The agent should read `.emw/prompts/README.md` and `00-session-start.md`.
4. If project-owned onboarding records are absent, the agent should automatically read and follow `01-project-onboarding.md`.
5. The onboarding prompt creates the project profile, ledgers, onboarding status, and project knowledge index using templates.
6. Review baseline assumptions and approve consequential decisions before implementation.

## Updating EMW
Update `.emw/` from the upstream repository using the Git remote steps above or a carefully managed copy process. Do not replace `.emw-project/` or `.project-knowledge/`. Merge changes to `AGENTS.md`, agent-specific instruction files, and OpenCode configuration rather than overwriting project-specific rules.

## Important limitation
EMW is a set of repository files and operating instructions, not a universal executable plugin. Agents can automatically read and follow prompt files only when their environment provides repository access and supports loading project instructions. Other agents may require you to paste the relevant prompt. The instructions influence behavior; they do not guarantee correctness or compliance.
