# EMW Prompt 02 — Feature Delivery

Use for a meaningful feature, enhancement, refactor, or bug fix with non-trivial behavior.

1. Read `AGENTS.md` and relevant project records.
2. Automatically perform knowledge retrieval using Prompt 07.
3. Inspect the actual implementation and tests before proposing changes.
4. Assess learning value, risk, demonstrated proficiency, novelty, complexity, and deadline pressure.
5. Read `.emw-project/mode-policy.yaml` (built-in defaults if absent) and the skill levels in `skill-ledger.yaml`. Propose the policy default mode for the weakest skill involved and explain why. If the human picks a mode with less practice, record their reason.
6. Define outcome, scope, non-goals, acceptance criteria, data contracts, permissions, edge cases, failure states, and verification plan.
7. Identify the concepts the human should own or demonstrate.
8. Agree on the plan before substantial implementation. Preserve human approval for sensitive or irreversible decisions.
9. Implement incrementally within scope. Record assistance level A0–A4.
10. Verify behavior and security; report checks actually run and checks not run.
11. Update project delivery records and mastery records separately. Add one entry to `.emw-project/task-log.yaml` (id, date, summary, mode, assistance, skills, mode_reason if needed) and run `python .emw/tools/emw_check.py`.
12. Use Prompt 08 to capture any durable, verified lesson. Do not create knowledge entries for trivial changes.

Completion report: outcome, files changed, decisions, checks/results, unresolved risks, knowledge retrieved/captured, assistance level, learning evidence, and next step.
