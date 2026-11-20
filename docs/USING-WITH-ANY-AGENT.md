# Using EMW with Any Coding Agent

EMW is agent-independent. The core rules are plain Markdown and YAML in `.emw/core/` and `.emw/templates/`. An agent uses EMW when it can read repository files and follow project instructions. No particular model, subscription, IDE, or vendor is required.

## The universal method
For any agent:
1. Open the project repository in the agent.
2. Make sure the agent can read the repository's root `AGENTS.md` and `.emw/` directory.
3. If the agent does not automatically load repository instructions, paste the short bootstrap prompt below.
4. Ask it to perform project reconnaissance before implementation.
5. Complete onboarding and baseline assessment.
6. For every meaningful task, require a mode selection, plan, verification, and separate delivery/mastery updates.

### Universal bootstrap prompt
Copy this into any coding agent:

> You are working in a repository that uses Engineering Mastery Workflow (EMW). Before changing code, read the root AGENTS.md and the relevant files in .emw/core/. Treat AGENTS.md and .emw/core/ as the operating contract. First inspect the repository and summarize its purpose, stack, architecture, conventions, tests, risks, and unknowns. Do not modify files yet. Identify the current task and assess learning value, risk, demonstrated proficiency, novelty, complexity, and deadline pressure. Recommend one of EMW's four collaboration modes with a short rationale. Keep engineering delivery and developer mastery separate. Never claim unrun checks passed or infer mastery from AI-generated code. Ask only for essential missing information. Then propose the smallest useful next step.

## Agent-specific setup

### OpenAI Codex and agents supporting AGENTS.md
- Keep `AGENTS.md` at repository root.
- For nested directories, add scoped `AGENTS.md` files only when local rules genuinely differ.
- Ask the agent to read `.emw/core/` for detailed policies.
- If it does not automatically read the root file, use the universal bootstrap prompt.

### Claude Code
- Keep `CLAUDE.md` at repository root. This repository includes one that points to `AGENTS.md`.
- Claude Code users can also use project-level settings and additional rules, but the core EMW source remains in `.emw/core/`.
- Start a session by asking Claude to inspect the repository and follow the EMW contract.

### Cursor
- This repository includes `.cursor/rules/emw.mdc`.
- Ensure project rules are enabled in Cursor.
- Keep detailed policies in `.emw/core/` and avoid duplicating the entire framework in the rule file.

### Gemini CLI
- Keep `GEMINI.md` at repository root. This repository includes a short pointer to `AGENTS.md`.
- Ask Gemini CLI to read the onboarding and core files before making changes.

### GitHub Copilot
- This repository includes `.github/copilot-instructions.md`.
- Copilot instruction loading varies by product surface and repository configuration. If the active surface does not load it, paste the universal bootstrap prompt and explicitly reference `AGENTS.md`.

### Other agents (Windsurf, Cline, Roo, Continue, Aider, etc.)
- Find the agent's documented repository instruction mechanism.
- Add a short instruction file using the same pattern as the included adapters.
- The adapter should point to `AGENTS.md` and `.emw/core/`, not fork or rewrite the rules.
- If no persistent instruction mechanism exists, use the universal bootstrap prompt at the start of each session.

## Daily usage prompts

### Start a new feature
> Use EMW. Analyze this feature before coding. Inspect relevant code, clarify requirements, assess L/R/P/N/C/D, select a collaboration mode, and produce acceptance criteria, a plan, edge cases, and verification strategy. Identify what I should implement or explain to develop mastery. Do not start implementation until the plan is clear.

### Learn a new technology while building
> Use EMW Mode 1 or 2 as appropriate. Assume my proficiency is unverified until assessed. Explain the minimum concepts needed for this task, connect them to the actual project without pretending different technologies are identical, and guide me through the implementation with progressive hints. Ask me to predict or explain important behavior.

### Delegate a bounded task
> Use EMW Mode 4 for this narrow task: [task]. Limit changes to [scope]. Preserve existing conventions. Do not change architecture or unrelated files. Run [checks]. Report files changed, assumptions, exact checks and results, and anything not verified.

### Review AI-generated code
> Audit this change under EMW. Inspect correctness, maintainability, security, authorization, tenant isolation, edge cases, and tests. Explain the most consequential decisions. Identify what I should be able to explain or modify independently. Do not treat generated tests as proof that the implementation is safe.

### Weekly mastery review
> Review the delivery and mastery ledgers separately. Summarize delivered work, concepts practiced, evidence-backed M0–M4 levels, AI assistance used, and 2–3 priority gaps. Give me one short independent exercise without its answer. Recommend next week's focus and one way to reduce AI assistance. Do not invent activity or mastery.

## Practical operating rhythm
- **Session start:** inspect current state and select a task.
- **Before coding:** agree on behavior, scope, risk, mode and tests.
- **During work:** ask for reasoning or independent implementation at the right moments.
- **Before completion:** run checks and report observed results.
- **At meaningful milestones:** update delivery and mastery records separately.
- **Weekly:** review evidence and choose a focused next learning opportunity.

## Keep it lightweight
Do not create a large ceremony for a typo or trivial formatting change. Use the full cycle for meaningful features, architectural changes, unfamiliar concepts, and risky work. EMW should reduce confusion and dependence, not slow every edit.

## Important limitation
Instruction files influence agent behavior; they do not guarantee compliance, correctness, security, or learning. Review important outputs, run tests, and retain human authority over consequential decisions.
