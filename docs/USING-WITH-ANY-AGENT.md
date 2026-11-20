# Using EMW with Any Coding Agent

EMW is agent-independent. Its core rules, knowledge, and prompts are repository files. Any agent that can inspect project files can use EMW; no particular model, IDE, subscription, or vendor is required.

## 1. One-time setup
Install `.emw/` and root `AGENTS.md` in your project. Add the instruction adapter for the agent you use. Preserve existing project instructions by merging rather than overwriting.

See [Installation](INSTALLATION.md) for copy and Git subtree approaches.

## 2. Automatic operation
The portable contract is `AGENTS.md`. It instructs compatible agents to:
1. Read `.emw/prompts/README.md` and `00-session-start.md` at session start.
2. Check project onboarding state. If project records are missing or stale, automatically read and follow `01-project-onboarding.md`.
3. Retrieve relevant shared and project knowledge before meaningful work using `07-knowledge-retrieval.md`.
4. Select task-specific prompts for features, learning, delegation, reviews, debugging, knowledge capture, and weekly reviews.
5. Update project records and capture verified knowledge when appropriate.

The prompts are separate files so humans can open and copy them. The agent should select and read them automatically when its repository instructions and file access permit. This is not an external function call or a model-training operation.

## 3. Agent-specific setup

### OpenAI Codex / agents supporting AGENTS.md
- Keep `AGENTS.md` at repository root.
- Keep detailed rules in `.emw/core/` and prompt routing in `.emw/prompts/README.md`.
- If the agent does not load repository instructions automatically, use [the universal bootstrap prompt](../.emw/prompts/00-bootstrap-any-agent.md).

### Claude Code
- Keep `CLAUDE.md` at repository root; this repository includes a pointer to `AGENTS.md`.
- Ensure Claude Code opens the target repository so it can read `.emw/`.
- Use the universal bootstrap prompt if the instruction file is not loaded in the active session.

### Cursor
- This repository includes `.cursor/rules/emw.mdc`.
- Ensure the project rule is enabled and the repository is opened as the workspace.
- Keep detailed policies and reusable prompts in `.emw/`.

### Gemini CLI
- Keep `GEMINI.md` at the repository root.
- Ask Gemini CLI to read `AGENTS.md` and `.emw/prompts/README.md` if these are not loaded by the active setup.

### OpenCode

- OpenCode natively loads root `AGENTS.md`; this is the primary EMW integration.
- Keep `opencode.json` and merge its `instructions` array if your project already has a config.
- OpenCode discovers skills in `.opencode/skills/` and slash commands in `.opencode/commands/`.
- This framework provides `@emw-workflow`, `@emw-knowledge`, and `@emw-mastery` skills plus `/emw-onboard`, `/emw-feature`, `/emw-learn`, `/emw-debug`, `/emw-review`, `/emw-weekly`, `/emw-capture`, and `/emw-practice` commands.
- See [OpenCode Integration](OPENCODE.md) for setup and examples.

### GitHub Copilot
- This repository includes `.github/copilot-instructions.md`.
- Instruction loading differs between Copilot surfaces and configurations. When it does not read repository instructions, use the universal bootstrap prompt.

### Other agents (Windsurf, Cline, Roo, Continue, Aider, etc.)
- Find the agent's documented repository-instruction mechanism.
- Add a short adapter that points to root `AGENTS.md`, `.emw/core/`, and `.emw/prompts/`.
- If no persistent instruction mechanism exists, paste [the universal bootstrap prompt](../.emw/prompts/00-bootstrap-any-agent.md) at session start and the relevant task prompt when needed.

## 4. Universal bootstrap prompt
The complete copyable prompt lives in [`.emw/prompts/00-bootstrap-any-agent.md`](../.emw/prompts/00-bootstrap-any-agent.md). It instructs an agent to load EMW, check onboarding state, retrieve knowledge, and follow the task-specific prompt library. Use it when a tool cannot load repository instruction files automatically.

## 5. Standalone prompt library
Open `.emw/prompts/README.md` for the routing table. Prompts include:
- Session start and project onboarding.
- Feature delivery and learning a technology.
- Bounded delegation, code review, and debugging.
- Knowledge retrieval and capture.
- Weekly mastery review.
- Shared knowledge contribution.

You can copy any prompt file directly into an agent chat. If the agent can read repository files and follows `AGENTS.md`, it should select applicable prompts without you pasting them.

## 6. Daily prompts (optional shortcuts)

### Start a feature
> Use EMW Prompt 02. Analyze this feature before coding, retrieve relevant knowledge, assess L/R/P/N/C/D, select a collaboration mode, and define acceptance criteria, plan, edge cases, tests, and the learning objective. Do not begin substantial implementation until the plan is clear.

### Learn while building
> Use EMW Prompt 03. Help me learn the minimum concepts needed for this project task. Use progressive hints, distinguish actual language/framework behavior, and assess my understanding independently from the code outcome.

### Delegate routine work
> Use EMW Prompt 04 for this narrow, low-risk task: [task]. Limit changes to [scope], run [checks], and report exact results and anything unverified.

### Review code
> Use EMW Prompt 05 to independently review this change. Prioritize concrete correctness, security, authorization, tenant-isolation, and regression findings.

### Debug
> Use EMW Prompt 06. Reproduce, form hypotheses, isolate root cause, add a regression check, and capture verified lessons. Do not present guesses as facts.

### Weekly review
> Use EMW Prompt 09. Review delivery and mastery separately, provide evidence-backed M0–M4 assessments, identify gaps, and give me an independent exercise without its answer.

## 7. Knowledge behavior
Before meaningful work, the agent retrieves from shared EMW knowledge in `.emw/knowledge/` and project knowledge in `.project-knowledge/`. After a durable, verified discovery, it captures project knowledge. It may propose generalizing the lesson for shared EMW, but must sanitize it and obtain human approval before publication. See [Knowledge System](KNOWLEDGE-SYSTEM.md).

## 8. Practical rhythm
- Session start: inspect current state and onboarding status.
- Before work: retrieve knowledge, assess risk and learning, select a mode.
- During work: use the task prompt and progressive assistance.
- Before completion: verify and report observed results.
- After meaningful work: update project records and capture durable knowledge.
- Weekly: review delivery, mastery, gaps, and knowledge quality.

## Limitations
Repository prompt files are not executable functions. Automatic prompt selection requires the agent to have repository access and follow its instructions. Knowledge retrieval is file-based; EMW does not automatically modify model weights. For large knowledge bases, add search tooling only when basic repository search becomes inadequate.
