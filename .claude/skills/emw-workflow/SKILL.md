---
name: emw-workflow
description: Use for meaningful software engineering tasks in an EMW-enabled repository. Applies the six-stage lifecycle, adaptive collaboration modes, human learning objectives, separate delivery and mastery tracking, and evidence-based verification.
---

# Engineering Mastery Workflow

This skill supplements the repository's root `AGENTS.md`. The root agent contract and `.emw/core/` documents remain canonical.

## Required behavior
1. Read root `AGENTS.md` and `.emw/prompts/README.md` if not already in context.
2. Detect whether this is the EMW framework repository or a consuming project.
3. In a consuming project, inspect onboarding records. If absent or stale, follow `.emw/prompts/01-project-onboarding.md` before feature work.
4. Before meaningful work, follow `.emw/prompts/07-knowledge-retrieval.md`.
5. Select the task prompt: feature delivery, learn technology, bounded delegation, review, debugging, knowledge capture, weekly review, or contribution.
6. Assess learning value, risk, demonstrated proficiency, novelty, complexity, and deadline pressure. Select a collaboration mode and explain why.
7. Use ANALYZE → SPECIFY & PLAN → EXECUTE → VERIFY → CONSOLIDATE → EVOLVE.
8. Keep engineering delivery and developer mastery separate.
9. Record AI assistance A0–A4. Promote M0–M4 only with evidence.
10. Never claim checks passed unless actually run.

## Collaboration modes
- Mode 1: Human-Led / Socratic.
- Mode 2: Co-Constructed / Plan-First.
- Mode 3: AI-Drafted / Guided Audit.
- Mode 4: Bounded Delegation.

## Knowledge behavior
Retrieve relevant entries from `.emw/knowledge/` and `.project-knowledge/`. Read the entries, not only their index metadata. Check applicability, version, status, confidence, evidence, and limitations. Capture durable verified discoveries in project knowledge. Never publish project-specific knowledge upstream without sanitization and human approval.

## Context loading
Do not load every EMW document for every task. Read the specific prompt and core policy relevant to the current work. For high-risk work, read the relevant verification and security guidance.

## Completion
Report files/behavior changed, checks run and not run, risks, knowledge used/captured, assistance level, mastery evidence or its absence, and next step.
