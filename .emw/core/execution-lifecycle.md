# Six-Stage Execution Lifecycle

## 1. ANALYZE
- Inspect repository, relevant files, architecture, stack, conventions and current state.
- Clarify the user problem and distinguish requirements from assumptions.
- Assess L/R/P/N/C/D and choose collaboration mode.
- Identify risks, dependencies, unknowns, and learning opportunities.

**Exit:** shared understanding of the task, scope, constraints, risks and collaboration mode.

## 2. SPECIFY & PLAN
- Define behavior, acceptance criteria and non-goals.
- Identify interfaces, data contracts, entities, permissions and state transitions.
- Write pseudocode or a sequence when logic is non-trivial.
- Consider failure paths, edge cases, observability, accessibility and security.
- Define tests and a small execution sequence.
- State the human learning objective if relevant.

**Exit:** an implementation-ready plan proportionate to task size.

## 3. EXECUTE
- Work in small increments.
- Keep changes within scope and follow repository conventions.
- Explain consequential changes; ask the human to own selected reasoning or implementation.
- Update the plan when discoveries change scope, and obtain approval for material changes.

**Exit:** implementation is ready for verification, with assumptions and deviations visible.

## 4. VERIFY
- Run relevant automated tests, type checks, linters, builds, migrations or manual checks.
- Review correctness, security, data integrity and regressions.
- Ask for an independent demonstration where mastery is a goal: explain, trace, debug, modify or implement.
- Distinguish observed results from checks not run.

**Exit:** evidence-based engineering status and, separately, learning evidence.

## 5. CONSOLIDATE
- Update delivery ledger with completed work, defects, decisions and remaining work.
- Update mastery ledger only when meaningful evidence exists.
- Capture durable lessons, commands, conventions, and unresolved questions.
- Record AI assistance level.

**Exit:** concise and accurate project and learning records.

## 6. EVOLVE
- Identify technical debt, architectural pressure, repeated friction and new skill gaps.
- Decide what should change in the workflow or project.
- Choose the next task with delivery and learning balanced.
- Retire stale records.

**Exit:** a prioritized next step, not an endless backlog.
