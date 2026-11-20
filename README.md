# Engineering Mastery Workflow (EMW)

**Build production software. Build the engineer who can build it again.**

Engineering Mastery Workflow (EMW) is a repository-native, agent-independent framework for human–AI software engineering. It pursues two outcomes together:

1. **Engineering delivery:** useful, secure, maintainable software that meets agreed requirements.
2. **Developer mastery:** evidence-backed growth in the human's ability to understand, implement, test, debug, explain, and evolve software independently.

EMW makes AI assistance deliberate and adaptive. It does not prohibit generated code, but it prevents task completion from being confused with human mastery.

## Start here

- [Using EMW with any coding agent](docs/USING-WITH-ANY-AGENT.md)
- [Installation guide](docs/INSTALLATION.md)
- [Knowledge system guide](docs/KNOWLEDGE-SYSTEM.md)
- [Root agent contract](AGENTS.md)
- [Automatic prompt library](.emw/prompts/README.md)
- [Core framework](.emw/core/)
- [Project onboarding template](.emw/templates/project-onboarding.md)

## The operating cycle

`ANALYZE → SPECIFY & PLAN → EXECUTE → VERIFY → CONSOLIDATE → EVOLVE`

Meaningful tasks are assessed for learning value, risk, demonstrated proficiency, novelty, complexity, and deadline pressure. EMW selects one of four collaboration modes:

| Mode | Human–AI relationship | Typical use |
|---|---|---|
| 1. Human-Led / Socratic | Human reasons and implements; AI coaches | High learning value, unfamiliarity, or low proficiency |
| 2. Co-Constructed / Plan-First | Agree on design and contracts; build together | New patterns, complex logic, unfamiliar integrations |
| 3. AI-Drafted / Guided Audit | AI drafts; human audits and demonstrates understanding | Familiar patterns with moderate learning value |
| 4. Bounded Delegation | AI executes narrow, low-risk work | Routine, well-understood tasks with clear checks |

## Core capabilities

### 1. Project Intelligence
Understand the repository, requirements, stack, architecture, conventions, risks, and current state before changing code.

### 2. Skill Intelligence
Map project-relevant skills, prerequisites, proficiency evidence, and knowledge gaps.

### 3. Task & Learning Orchestration
Select the collaboration mode and human learning objective for each meaningful task.

### 4. Collaborative Execution
Use Socratic guidance, plan-first pairing, guided AI drafts, or bounded delegation as appropriate.

### 5. Verification & Mastery
Verify software behavior separately from the developer's ability to explain, implement, modify, and debug it independently.

### 6. Knowledge Intelligence Layer
Retrieve reusable shared and project-specific knowledge before work; capture verified lessons after meaningful discoveries; review contributions before promoting generalized knowledge to the shared EMW repository.

## Two ledgers, never one

- **Engineering Delivery Ledger:** requirements, features, decisions, implementation, tests, defects, and technical debt.
- **Developer Mastery Ledger:** technologies/concepts, M0–M4 levels, evidence, assistance used, gaps, and next assessments.

A completed feature is delivery evidence, not automatic mastery evidence.

## Proficiency scale

- **M0 — Unknown:** no reliable evidence yet.
- **M1 — Awareness:** recognizes the concept and explains its basic purpose.
- **M2 — Guided Application:** applies it with examples, hints, or AI assistance.
- **M3 — Independent Application:** implements, explains, tests, and debugs without solution-level assistance.
- **M4 — Transfer & Mastery:** handles unfamiliar variations, compares alternatives, explains limitations, and teaches the concept.

## Persistent knowledge

EMW keeps two distinct knowledge stores:
- Shared, reviewed knowledge in `.emw/knowledge/`.
- Project-specific knowledge in the consuming repository's `.project-knowledge/`.

The project knowledge base is not automatically published upstream. Shared contributions require evidence, sanitization, and human approval. Knowledge entries record source, status, confidence, applicability, limitations, and review metadata.

## Automatic prompts

Standalone prompts live in `.emw/prompts/`. The root `AGENTS.md` tells compatible agents to select them automatically based on task triggers. Examples include session start, project onboarding, feature delivery, debugging, knowledge retrieval/capture, code review, and weekly mastery review.

Automatic loading depends on the agent being able to read repository files and follow project instructions. When an agent cannot do so, copy the relevant prompt into its chat.

## Repository structure

```text
.
├── AGENTS.md
├── CLAUDE.md / GEMINI.md
├── .cursor/rules/emw.mdc
├── .github/copilot-instructions.md
├── .emw/
│   ├── core/                 # Agent-independent EMW rules
│   ├── prompts/              # Standalone, task-triggered prompts
│   ├── knowledge/            # Shared curated knowledge and index
│   ├── templates/            # Reusable record templates
│   ├── assessments/          # Evidence-gathering exercises
│   └── examples/
├── docs/
│   ├── INSTALLATION.md
│   ├── USING-WITH-ANY-AGENT.md
│   └── KNOWLEDGE-SYSTEM.md
└── CONTRIBUTING.md
```

A consuming project keeps its live project records in `.emw-project/` and project knowledge in `.project-knowledge/`, separate from upstream framework files.

## Design principles

- Preserve human ownership of requirements and consequential decisions.
- Start with reasoning, contracts, and pseudocode when warranted.
- Match assistance to demonstrated proficiency.
- Use productive struggle, not punitive withholding.
- Verify AI-generated code independently, especially in high-risk areas.
- Preserve provenance and distinguish evidence from assumptions.
- Keep records concise and useful; do not log every trivial edit.
- Treat EMW as a framework to evaluate and improve, not a guarantee of mastery.

## Status

EMW v1.1 is a documentation-first framework with a prompt-routing system and a governed, file-based knowledge architecture. It does not require a specific language, model, IDE, agent, or vector database. Indexing and retrieval can begin with normal repository search; add automation only when actual usage justifies it.

## License

No license has been declared. Add a license before redistributing this repository under terms you intend others to rely on.
