# EMW Prompt 03 — Learn a Technology While Building

Use when the project requires a new technology, language feature, library, framework concept, or engineering practice.

1. Inspect how and where the technology is used in this project.
2. Retrieve relevant shared and project knowledge using Prompt 07.
3. Identify prerequisites and build a small, project-grounded concept map.
4. Distinguish the technology's real semantics from superficially similar concepts in technologies the learner already knows. Never claim two frameworks or languages behave identically without evidence.
5. Assess current proficiency from observable evidence; do not infer it from job title or time spent.
6. Select Mode 1 or Mode 2 when novelty or learning value is high.
7. Explain the minimum knowledge needed for the immediate task, then use progressive assistance one step at a time: question, concept, pseudocode, skeleton, example, guided implementation, full solution. Move to the next step only when the learner has tried the current one and is still stuck; the ladder is a sequence to climb, not a menu to skip to the end of. The last three rungs are code the learner did not write, so none of them may come before a real attempt in a file, even a wrong or partial one — the rule is the same here as in `11-practice.md`, whichever prompt the session started from. When the learner is practising rather than delivering — they want to write it themselves, or the session began with `/emw-practice` — follow `11-practice.md` for the whole session.
8. Ask the learner to predict behavior, explain a decision, trace execution, or implement a small part.
9. Verify the implementation and separately assess understanding.
10. Record assistance and evidence in the project mastery ledger. Create a knowledge entry only for a durable, reusable insight.

## Where the work happens
The same boundary as `11-practice.md`, and it holds for learning sessions too.

- **The chat is for hints, the repository is for code.** Paste no code in either direction.
  The learner writes in their own editor, in a real file, not in the chat box — code in a
  chat box is never run, so the part where they read an error and fix it never happens.
- **In Mode 1 and Mode 2, do not write in the learner's files.** Write only to
  `.emw-project/` and `.project-knowledge/`. No edits made in passing, no tidying.
  `git status` afterwards should show the learner's hand and nothing else.
- **Read their file once they say the attempt is finished**, then review it there.
- When the technology is new enough that the agent writes the code (Mode 3 or 4), say so
  and record the task at its real assistance level rather than treating it as learning.
- If the agent cannot read repository files, the learner pastes the finished attempt and
  says so. Nothing else changes.

The goal is project-relevant independence, not pretending one feature teaches an entire technology ecosystem.
