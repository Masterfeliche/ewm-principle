# Developer Mastery Framework

## Proficiency levels

| Level | Name | Observable description |
|---|---|---|
| M0 | Unknown | No reliable evidence of understanding or use. |
| M1 | Awareness | Recognizes the concept and can explain its basic purpose with support or after instruction. |
| M2 | Guided Application | Can apply the concept with examples, hints, documentation guidance, or AI assistance. |
| M3 | Independent Application | Can implement, explain, test, debug, and modify it without solution-level assistance. |
| M4 | Transfer & Mastery | Can handle unfamiliar variants, compare alternatives, explain trade-offs and limitations, and teach the concept. |

## Evidence types
- **Explain:** describe purpose, mechanics, boundaries and trade-offs.
- **Predict:** forecast output, state changes, or failure behavior before execution.
- **Trace:** follow execution or data through the system.
- **Debug:** isolate a defect and justify the fix.
- **Implement:** create a working solution without solution-level assistance.
- **Modify:** safely change an existing solution or add a requirement.
- **Transfer:** solve a related but unfamiliar problem.
- **Rebuild:** recreate something you built earlier from memory, without notes or AI, after a gap of days. Used by learning-track gates.
- **Teach:** explain the concept clearly enough for another developer to use it.

Evidence should identify the task, date, context, assistance used, and observed result. A short assessment can be more useful than a long claim.

## Assistance labels
- **A0:** independent; no solution-level AI help (ordinary docs/tooling are allowed and should be noted).
- **A1:** conceptual hint or clarification.
- **A2:** pseudocode, decomposition, or targeted example.
- **A3:** AI-provided skeleton, focused code, or guided pair implementation.
- **A4:** AI-generated implementation substantially authored by the agent.

A3/A4 work can still produce learning, but it does not by itself demonstrate M3.

## Promotion guidance
- M0 → M1: explain what the concept is for and identify where it appears.
- M1 → M2: apply it successfully with guidance and explain the guided steps.
- M2 → M3: independently implement, test, explain, and debug a representative task.
- M3 → M4: demonstrate transfer to an unfamiliar case, compare alternatives, and explain limitations.

No automatic promotion based on task completion, repetition, elapsed time, or AI-generated tests. No automatic demotion based only on time; old evidence may be marked stale or lower-confidence and reassessed.

## Who verified the evidence
Each evidence item records `verified_by`:
- **self:** the developer and agent recorded it. Useful, but the agent is assessing its own coaching.
- **human:** a lead, peer or reviewer saw the demonstration or reviewed the work.

M3 and M4 require at least one A0–A2 evidence item with `verified_by: human`. An agent may run and record assessments but cannot be the only judge of independent mastery.

## Recall checks
Spacing retrievals out over days is what makes a skill stick; re-reading code is not retrieval. EMW schedules a short check from memory 2, 7 and 30 days after a skill's first evidence (`recall_days` in `.emw-project/mode-policy.yaml`; `[]` turns them off). `python .emw/tools/emw_recall.py due` lists what is owed, `plan` shows the whole schedule, and `done` records the result; `emw_check` prints a due check as a NOTE, which never fails a build. A check counts only as evidence of type `recall` or `rebuild` at A0–A1, dated inside its window. A rebuild that needed the old code means the level was not real: lower it. See `.emw/prompts/13-recall.md`.

## Assessment cadence
Checks without AI are sampled, not run on every task. `.emw-project/mode-policy.yaml` sets `assessment_every` (default 4): after that many logged tasks touch a skill with no new A0–A2 evidence, `emw_check` warns and the agent offers a short check from `.emw/assessments/` or a Prompt 11 practice session. Keep checks short (10–20 minutes): predict, trace, fix a planted bug, or rebuild from memory. Skills at M4 are exempt.

## Scope of mastery
- **S1 — Project Mastery:** concepts actually used and needed to independently maintain or extend this project.
- **S2 — Foundational Mastery:** essential language/runtime and engineering foundations that the project may not naturally exercise.
- **S3 — Ecosystem Literacy:** relevant adjacent tools and advanced capabilities; know what they do, when they apply, and where to consult authoritative documentation.

Do not claim mastery of an entire language or framework from a narrow project feature.

## Skill map fields
Each skill node should include: stable ID, name, technology, scope, prerequisites, target level, current estimate, confidence, evidence references, last assessed, and next assessment. Track only useful project-relevant concepts.

## Confidence
Use high / medium / low confidence. Low confidence means evidence is narrow, old, heavily assisted, or ambiguous. Prefer "unverified" when there is no evidence.
