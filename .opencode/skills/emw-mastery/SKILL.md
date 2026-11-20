---
name: EMW Developer Mastery
description: Use when teaching a technology during project work, assessing developer proficiency, planning independent exercises, or reviewing weekly learning progress under EMW.
---

# EMW Developer Mastery

Follow `.emw/core/mastery-framework.md`, `.emw/core/collaboration-modes.md`, and relevant prompt files.

## Principles
- Project completion and human mastery are different outcomes.
- Assess the specific concept, not a broad technology label.
- Use evidence, not confidence or self-rating alone.
- Record assistance A0–A4.
- No promotion based only on AI-generated code, elapsed time, or passing tests.

## Levels
- M0 Unknown.
- M1 Awareness.
- M2 Guided Application.
- M3 Independent Application.
- M4 Transfer & Mastery.

## Evidence
Use explanation, prediction, tracing, debugging, independent implementation, modification, transfer, or teaching. Record what the human did, what AI supplied, and the observed result.

## Teaching
Use progressive assistance: Socratic question → concept explanation → pseudocode → skeleton/diff → example → guided implementation → complete worked solution. Do not obstruct the learner when stronger help is needed.

## Assessing
Pair verbal explanations with practical evidence for M3/M4. Use the assessment prompts in `.emw/assessments/`. Keep the developer mastery ledger separate from the engineering delivery ledger.

## Practice and checks without AI
- For hands-on learning, follow `.emw/prompts/11-practice.md`: the developer types the solution; give hints one step at a time and no complete solution before an attempt.
- When `emw_check` reports a skill overdue, offer a short check from `.emw/assessments/` or a practice session.
- Record `verified_by: self` unless a human lead or peer saw the work. M3/M4 need one human-verified A0–A2 item.
