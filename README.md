# Engineering Mastery Workflow (EMW)

**Build production software. Build the engineer who can build it again.**

Engineering Mastery Workflow (EMW) is a repository-native, agent-independent operating framework for human–AI software engineering. It is designed to achieve two outcomes in parallel:

1. **Engineering delivery:** useful, secure, maintainable software that meets agreed requirements.
2. **Developer mastery:** evidence-backed growth in the human developer's ability to understand, implement, test, debug, explain, and evolve that software independently.

EMW does not prohibit AI-generated code. It makes the level of assistance deliberate, appropriate to the task, visible, and progressively reduced as the developer gains competence.

## Start here

- Read [the operating guide](docs/USING-WITH-ANY-AGENT.md).
- Add the framework to a project using [the installation guide](docs/INSTALLATION.md).
- Read the root [AGENTS.md](AGENTS.md), which contains the portable agent contract.
- Use [the core framework](.emw/core/) as the source of truth.
- Start a project with [.emw/templates/project-onboarding.md](.emw/templates/project-onboarding.md).

## The EMW operating cycle

`ANALYZE → SPECIFY & PLAN → EXECUTE → VERIFY → CONSOLIDATE → EVOLVE`

Every meaningful task is assessed for learning value, risk, novelty, complexity, and demonstrated proficiency. EMW then selects one of four collaboration modes:

| Mode | Working relationship | Typical use |
|---|---|---|
| 1. Human-Led / Socratic | Human reasons and implements; AI coaches and challenges | New, high-learning-value, or high-risk work |
| 2. Co-Constructed / Plan-First | Agree on design and contracts; build in partnership | New patterns, complex logic, unfamiliar integrations |
| 3. AI-Drafted / Guided Audit | AI drafts within known patterns; human audits and demonstrates understanding | Familiar patterns with moderate learning value |
| 4. Bounded Delegation | AI executes a narrow, low-risk, well-understood task | Routine work with clear boundaries and checks |

## Two ledgers, never one

EMW tracks project progress separately from developer progress:

- **Engineering Delivery Ledger:** requirements, features, decisions, implementation, tests, defects, and technical debt.
- **Developer Mastery Ledger:** skills encountered, proficiency levels, evidence, assistance used, gaps, and next assessments.

A merged feature is evidence of delivery. It is not, by itself, evidence of mastery.

## Proficiency scale

- **M0 — Unknown:** no reliable evidence yet.
- **M1 — Awareness:** can recognize the concept and explain its basic purpose.
- **M2 — Guided Application:** can use it with examples, hints, or AI assistance.
- **M3 — Independent Application:** can implement, explain, test, and debug it without solution-level assistance.
- **M4 — Transfer & Mastery:** can handle unfamiliar variations, compare alternatives, explain limitations, and teach the concept.

Levels require evidence. Do not promote a skill merely because code exists in the repository.

## Repository structure

```text
.
├── AGENTS.md                         # Portable root agent instructions
├── CLAUDE.md                         # Claude Code entry point
├── GEMINI.md                         # Gemini CLI entry point
├── .cursor/rules/emw.mdc             # Cursor project rule
├── .github/copilot-instructions.md   # GitHub Copilot instructions
├── .emw/
│   ├── core/                         # Agent-independent operating framework
│   ├── templates/                    # Project, task, learning and review records
│   ├── assessments/                  # Evidence-gathering exercises
│   └── examples/                     # Illustrative examples
└── docs/
    ├── INSTALLATION.md
    └── USING-WITH-ANY-AGENT.md
```

## Design principles

- Preserve human ownership of requirements, trade-offs, and consequential decisions.
- Start with reasoning, requirements, contracts, and pseudocode when the task warrants it.
- Match assistance to demonstrated proficiency; do not assume a beginner or expert.
- Use productive struggle, not punitive withholding. The developer may request a worked explanation.
- Verify generated code adversarially, especially security, authorization, tenancy, and payment behavior.
- Record what was independently demonstrated separately from what was AI-guided.
- Keep persistent records concise, factual, and useful; do not log every trivial edit.
- Treat this as a practical framework to evaluate and improve, not a scientifically validated guarantee of mastery.

## Status

EMW v1.0 is a documentation-first operating framework. It intentionally does not require a particular language, model provider, IDE, agent, framework, or project-management tool. Automation and dashboards should be added only when real use demonstrates that they solve a problem.

## License

No license has been declared yet. Add a license before redistributing this repository under terms you intend others to rely on.
