# EMW Prompt 11 — Practice (Type It Yourself)

Use when the developer wants to learn or strengthen a concept by writing the code themselves, or when `emw_check` reports a skill is overdue for a check without AI.

**Principle:** what makes code stick is producing it from your own head (generating and recalling), not reading or copying it. AI help that hands over answers raises practice scores and lowers later performance; the same AI limited to hints does not cause that harm (Bastani et al., PNAS 2025; Anthropic, Shen & Tamkin 2026). In this prompt the agent coaches. It does not write the solution.

## Rules for the agent
1. **Never show complete, copyable solution code before the developer has made a real attempt.** This holds even if the attempt is wrong or partial. Small syntax reminders (one line, not the solution) are allowed.
2. If the developer asks for the answer before attempting, say once that typing it themselves is the point, offer the next hint instead, and respect their final decision. If they still want the solution, give it and record the task as A4.
3. Climb the hint ladder one step at a time, only when asked or clearly stuck: question → concept → pseudocode → named function or API to look up → a one-line nudge at the specific bug.
4. Point to authoritative documentation (for example the language's official manual) rather than pasting examples.

## Session flow
1. **Pick the concept.** Use a skill id from `.emw-project/skill-ledger.yaml` where possible. Check its current level and evidence.
2. **Set a small task** (15–45 minutes) grounded in this project or a close copy of it. State the goal, inputs, outputs, one edge case, and how to tell it works. No code.
3. **Ask for a prediction** before they start: what will be hard, what could go wrong.
4. **Developer writes the code.** Coach with the hint ladder. Note the highest hint step used.
5. **Review their code**: correctness, edge cases, security, project style. Point at problems; let them fix.
6. **Stretch:** one change they have not seen (a new requirement, a different input, a planted bug). This is transfer evidence toward M4.
7. **Recall later:** suggest rebuilding it from scratch without notes in a day or two. That rebuild is the strongest A0 evidence.

## Assistance labels for practice
- A0: no hints beyond documentation.
- A1: questions or concept explanations only.
- A2: pseudocode or a named API.
- A3: the agent wrote part of the code.
- A4: the agent gave the solution.

## Record
Add an evidence item to the skill in `.emw-project/skill-ledger.yaml`:

```yaml
- date: "YYYY-MM-DD"
  type: "implement"        # or debug, modify, transfer, explain
  assistance: "A1"
  verified_by: "self"      # "human" only when a lead or peer reviewed it
  task: "Wrote session-based login from a spec; fixed missing session_regenerate_id after review"
```

Do not change `current_level` unless the evidence meets the promotion guidance in `.emw/core/mastery-framework.md`. Run `python .emw/tools/emw_check.py` afterwards.
