# OpenCode Integration

EMW works with OpenCode through its native repository instruction support and this repository's OpenCode-specific skills, commands, and configuration.

## What OpenCode loads
- Root `AGENTS.md`: OpenCode's native project-instruction mechanism. It is the canonical EMW contract.
- `opencode.json`: explicitly loads the EMW knowledge policy and prompt-routing index as additional instructions.
- `.opencode/skills/`: exposes the EMW workflow, knowledge, and developer-mastery skills for the agent to load when relevant.
- `.opencode/commands/`: provides reusable slash commands for common EMW workflows.

OpenCode also supports a `CLAUDE.md` fallback when no `AGENTS.md` is present, but this repository has `AGENTS.md`, so that is the applicable project instruction file.

Official references:
- [OpenCode Instructions](https://opencode.ai/docs/instructions)
- [OpenCode Skills](https://opencode.ai/docs/skills)
- [OpenCode Commands](https://opencode.ai/docs/commands)
- [OpenCode Configuration](https://opencode.ai/docs/config)

## Use EMW with OpenCode
1. Install EMW into your project using [the installation guide](INSTALLATION.md).
2. Open the project root in OpenCode, not a nested folder outside the repository.
3. Confirm that the root AGENTS.md and opencode.json are present.
4. Start a new OpenCode session so the workspace instructions and configuration are loaded.
5. The agent should read the session-start prompt, inspect onboarding status, and load the relevant task prompt and knowledge.

Do not copy this framework repository's entire root into a consuming project without following the installation guide. In a consuming project, place the framework under `.emw/`, copy/merge `AGENTS.md` into the project root, and merge `opencode.json` settings if the project already has one.

## Available slash commands

| Command | Purpose |
|---|---|
| `/emw-onboard [focus]` | Initialize the project's EMW profile, ledgers, and project knowledge base. |
| `/emw-feature [feature]` | Plan and execute a feature using EMW modes and the full lifecycle. |
| `/emw-learn [technology or concept]` | Learn a technology while implementing project work. |
| `/emw-debug [problem]` | Investigate a defect and capture verified diagnostic lessons. |
| `/emw-review [file, diff, or PR]` | Independently review correctness, security, and tests. |
| `/emw-weekly [period]` | Review delivery and developer mastery separately. |
| `/emw-capture [discovery]` | Capture a durable, verified lesson in project knowledge. |

Commands are prompt templates. They do not run tests or change files on their own; the agent interprets the command and uses its available tools.

## Available OpenCode skills

- `@emw-workflow`: apply the EMW lifecycle, collaboration modes, verification, and dual ledgers.
- `@emw-knowledge`: retrieve and capture project/shared knowledge with provenance and governance.
- `@emw-mastery`: teach, assess, and track developer proficiency with evidence.

OpenCode advertises discovered skills to the agent. The agent can load a skill when relevant; you can explicitly request one using its `@skill-id`. If a skill does not appear, check that the project is opened correctly, skill discovery is enabled, and the selected agent has permission to use skills.

## Automatic versus explicit use
- **Automatic instructions:** OpenCode loads `AGENTS.md` and the extra instruction paths configured in `opencode.json`.
- **Automatic skill discovery:** OpenCode discovers project skills under `.opencode/skills/`; the agent decides when a relevant skill is needed.
- **Explicit commands:** the user invokes `/emw-feature`, `/emw-debug`, and other commands for deterministic task-specific workflows.
- **Fallback:** if agent instructions or file access are unavailable, paste `.emw/prompts/00-bootstrap-any-agent.md` and the relevant task prompt.

## Existing OpenCode configuration

EMW's `opencode.json` adds instruction paths. If your project already has an OpenCode configuration, merge the `instructions` array into it rather than overwriting your configuration. Preserve your model, provider, permissions, MCP servers, plugins, tools, and other settings.

## Suggested first run

Open the consuming project in OpenCode and run:

```text
/emw-onboard
```

Review the resulting profile and baseline. Then try:

```text
/emw-feature <first real feature>
```

Use `/emw-weekly` after meaningful work has accumulated.

## Limitations

OpenCode integration does not train or modify a model's weights. Skills and knowledge files provide persistent, retrievable context. Agent behavior still depends on the selected model, configured permissions, available tools, and instruction compliance. Always verify important changes and retain human approval for consequential decisions.