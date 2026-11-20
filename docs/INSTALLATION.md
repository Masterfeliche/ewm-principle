# Installing EMW in a Project

EMW is installed in the repository it governs. The shared framework files and the project's own working records must remain separate.

## Recommended: copy or vendor the framework
1. Copy the framework's `.emw/` directory into the target repository.
2. Copy root `AGENTS.md` to the target root.
3. Copy the relevant adapter: `CLAUDE.md`, `GEMINI.md`, `.cursor/rules/emw.mdc`, or `.github/copilot-instructions.md`.
4. If the target already has an agent instruction file, merge the EMW reference into it; never blindly overwrite existing project instructions.
5. Copy `.emw/templates/README-project-state.md` as a guide. The onboarding prompt will create project-owned `.emw-project/` and `.project-knowledge/` records.
6. Commit the framework integration.

## Git subtree option
From the target project repository, where `.emw/` does not already contain conflicting framework files:

```bash
git remote add emw https://github.com/Masterfeliche/ewm-principle.git
git fetch emw
git subtree add --prefix=.emw emw main --squash
```

Copy or merge the root agent instruction files separately. Keep project records outside `.emw/` so upstream updates cannot overwrite them.

To update the framework later:

```bash
git fetch emw
git subtree pull --prefix=.emw emw main --squash
```

If the `emw` remote already exists, do not add it again. If the target already has an `.emw/` directory, inspect and merge it carefully before using subtree; do not overwrite local framework modifications or project data.

## Project-owned locations
A consuming repository should have:

```text
project/
├── AGENTS.md
├── .emw/                         # Shared framework files, updated from upstream
│   ├── core/
│   ├── prompts/
│   ├── knowledge/                # Shared, curated EMW knowledge
│   └── templates/
├── .emw-project/                 # This project's own status and ledgers
│   ├── onboarding-status.yaml
│   ├── project-profile.md
│   ├── delivery-ledger.md
│   └── skill-ledger.yaml
├── .project-knowledge/           # This project's own durable knowledge
│   ├── README.md
│   ├── index.yaml
│   ├── architecture/
│   ├── business-rules/
│   ├── integrations/
│   ├── debugging/
│   └── security/
└── src/
```

This separation is intentional: shared framework updates should not replace project-specific ledgers or knowledge.

## First session and automatic onboarding
1. Open the repository in an agent that can read its files.
2. Ensure the root `AGENTS.md` is loaded. If the agent does not auto-load it, paste the universal bootstrap prompt from [Using EMW with Any Agent](USING-WITH-ANY-AGENT.md).
3. The agent should read `.emw/prompts/README.md` and `00-session-start.md`.
4. If project-owned onboarding records are absent, the agent should automatically read and follow `.emw/prompts/01-project-onboarding.md`.
5. The onboarding prompt creates the project profile, ledgers, onboarding status, and project knowledge index using templates.
6. Review baseline assumptions and approve consequential decisions before implementation.

## Updating EMW
Update `.emw/` from the upstream repository using your chosen vendor, subtree, or carefully managed copy process. Do not replace `.emw-project/` or `.project-knowledge/`. Merge changes to `AGENTS.md` and agent-specific instruction files rather than overwriting project-specific rules.

## Important limitation
EMW is a set of repository files and operating instructions, not an executable plugin. Agents can automatically read and follow prompt files only when their environment gives them repository access and supports loading project instructions. Other agents may require you to paste the relevant prompt manually. The instructions influence behavior; they do not guarantee correctness or compliance.
