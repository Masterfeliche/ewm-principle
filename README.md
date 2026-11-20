# Engineering Mastery Workflow (EMW)

**Build production software. Build the engineer who can build it again.**

Engineering Mastery Workflow (EMW) is a repository-native, agent-independent framework for human–AI software engineering. It pursues two outcomes together:

1. **Engineering delivery:** useful, secure, maintainable software that meets agreed requirements.
2. **Developer mastery:** evidence-backed growth in the human's ability to understand, implement, test, debug, explain, and evolve software independently.

EMW makes AI assistance deliberate and adaptive. It does not prohibit generated code, but it prevents task completion from being confused with human mastery.

## Who it is for
- **Junior developers** who want AI help without skipping the part where they learn.
- **Anyone learning a new stack on the job**: a new language, framework or codebase.
- **Team leads and mentors** onboarding people, who need to know what each developer can do without the AI, not just what they shipped.
- **Teams asking where their next seniors will come from** when routine implementation is increasingly done by AI.

Experienced developers working in code they know well need it least; the quick path in `AGENTS.md` keeps it out of their way.

## The problem it addresses
Early research points the same way, though the studies are small and recent:
- Developers learning a new library with AI scored 50% vs 67% on a follow-up quiz, with the largest gap in debugging. Those who asked for explanations kept more than those who delegated the code ([Anthropic, 2026](https://www.anthropic.com/research/AI-assistance-coding-skills)).
- Students with unrestricted AI did better in practice and 17% worse on the exam afterwards; a version limited to hints avoided the harm ([Bastani et al., PNAS 2025](https://ideas.repec.org/a/nas/journl/v122y2025pe2422633122.html)).
- Experienced developers were 19% slower with AI on their own repositories yet believed they were 20% faster ([METR, 2025](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/)).

EMW responds with help limits set by team policy rather than chosen task by task, evidence-based skill records, and sampled checks without AI. Whether EMW itself improves outcomes is not yet measured; see the [pilot study method](docs/research/pilot.md).

## Start here
- [Using EMW with any coding agent](docs/USING-WITH-ANY-AGENT.md)
- [OpenCode setup and commands](docs/OPENCODE.md)
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
1. **Project Intelligence:** understand the repository, requirements, stack, architecture, conventions, risks, and current state.
2. **Skill Intelligence:** map project-relevant skills, prerequisites, proficiency evidence, and knowledge gaps.
3. **Task & Learning Orchestration:** select a collaboration mode and human learning objective.
4. **Collaborative Execution:** use Socratic guidance, plan-first pairing, guided AI drafts, or bounded delegation.
5. **Verification & Mastery:** verify software behavior separately from the developer's ability to explain, implement, modify, and debug independently.
6. **Knowledge Intelligence:** retrieve reusable shared and project knowledge; capture verified lessons; review contributions before promoting generalized knowledge.

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

## Learning tracks
A track is a staged path for one language: skills with target levels, one project per stage, and a gate for moving on. The shared core (Stage 0) and four tracks (PHP with Laravel, .NET, Go, and Python), with projects set in Tanzania and East Africa, are in `.emw/tracks/`; see [the tracks README](.emw/tracks/README.md). Start one with `python .emw/tools/emw_track.py start php` or `/emw-track start php`; `status` shows where you are and `next` opens the next stage once its gate is met.

## Validating records
`python .emw/tools/emw_check.py` checks knowledge entries against the JSON schemas, keeps `index.yaml` in step with the entry files, and, in a consuming project, checks the onboarding status and skill ledger (for example, M3 or M4 needs evidence produced with assistance A0–A2). It needs Python 3.9+ and PyYAML, exits non-zero on errors, and `--strict` also fails on warnings. `.github/workflows/emw-check.yml` runs it, plus the checker's own tests, on every pull request; copy it into consuming projects to enforce the records there.

## Persistent knowledge
EMW keeps two distinct knowledge stores:
- Shared, reviewed knowledge in `.emw/knowledge/`.
- Project-specific knowledge in the consuming repository's `.project-knowledge/`.

The project knowledge base is not automatically published upstream. Shared contributions require evidence, sanitization, and human approval.

## Agent integrations
- Codex and other AGENTS.md agents: root `AGENTS.md`.
- Claude Code: `CLAUDE.md` adapter, slash commands in `.claude/commands/`, skills in `.claude/skills/`.
- Gemini CLI: `GEMINI.md` adapter.
- Cursor: `.cursor/rules/emw.mdc`.
- GitHub Copilot: `.github/copilot-instructions.md`.
- OpenCode: native `AGENTS.md` discovery, `opencode.json`, `.opencode/skills/`, and `.opencode/commands/`.

Claude Code and OpenCode users can invoke `/emw-onboard`, `/emw-feature`, `/emw-learn`, `/emw-debug`, `/emw-review`, `/emw-weekly`, `/emw-capture`, `/emw-practice`, and `/emw-track`. See [OpenCode setup](docs/OPENCODE.md).

## Repository structure

```text
.
├── AGENTS.md
├── CLAUDE.md / GEMINI.md
├── opencode.json
├── .opencode/
│   ├── skills/
│   └── commands/
├── .claude/
│   ├── commands/
│   └── skills/
├── .github/workflows/      # CI: emw_check --strict + checker tests
├── .cursor/rules/emw.mdc
├── .github/copilot-instructions.md
├── .emw/
│   ├── tracks/               # Learning tracks: core, PHP, .NET, Go, Python, with project briefs
│   ├── core/                 # Agent-independent EMW rules
│   ├── prompts/              # Standalone, task-triggered prompts
│   ├── knowledge/            # Shared curated knowledge and index
│   ├── templates/            # Reusable record templates
│   ├── tools/                # emw_check.py validator and its tests
│   ├── assessments/
│   └── examples/
└── docs/
```

A consuming project keeps live project records in `.emw-project/` and project knowledge in `.project-knowledge/`, separate from upstream framework files.

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
EMW v1.1 is a documentation-first framework with a prompt-routing system, OpenCode-native skills and commands, and a governed file-based knowledge architecture. It does not require a specific language, model, IDE, agent, or vector database. Indexing and retrieval can begin with normal repository search; add automation only when actual usage justifies it.

## License
No license has been declared. Add a license before redistributing this repository under terms you intend others to rely on.