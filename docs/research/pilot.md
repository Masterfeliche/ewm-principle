# EMW Pilot Study Method

**Question:** when developers learn something new with AI help, do they understand it better afterwards if the AI follows EMW Modes 1–2 than if they use AI freely?

This copies the design of Anthropic's 2026 randomized trial ([Shen & Tamkin](https://arxiv.org/html/2601.20245v1)), which found a 50% vs 67% quiz gap between AI-assisted and hand-coding groups, largest on debugging. Here both groups use AI; only the way they use it differs.

> A pilot with 8–12 people cannot prove anything statistically. Its job is to show whether the effect looks worth a larger study, and to surface practical problems with EMW. Report it that way.

## 1. Hypotheses (write these down before running)
- **H1:** the EMW group scores higher on the quiz without AI, especially on debugging questions.
- **H2:** the EMW group takes longer on the task. Record how much; a cost is expected.
- **H3:** the free-AI group rates its own learning higher relative to its quiz score than the EMW group does (the perception gap METR and Bastani et al. observed).

Fill in `pilot-results-template.md` with these before the first session, and don't change them afterwards.

## 2. Participants
- 8–12 developers, ideally juniors, all **unfamiliar with the chosen library**. Ask; exclude anyone who has used it.
- Randomly assign to two equal groups (for example, shuffle names with a coin flip or `python -c "import random"`). Don't let people choose.
- Get consent. State in writing that results are anonymous and **never used in performance reviews**.

## 3. Materials
- **One library** none of them know, in a language they all use. Pick something with real concepts to misunderstand (async, an ORM's lazy loading, a state machine library), not a thin wrapper.
- **One task**, 35–45 minutes, with automated tests that say whether it works.
- **One quiz** (`pilot-quiz-template.md`): 10 questions, 4 debugging, 3 code reading, 3 concepts. Write it before the sessions and keep it hidden.
- **Same AI tool and model for both groups.**

| Group | Setup |
|---|---|
| Free AI | Plain agent, no EMW files. Told: "Use AI however you like." |
| EMW | Repository with EMW installed; the library's skill set to M0 in the skill ledger, so the mode policy defaults to Mode 1. The agent proposes modes and gives hints; participants may override with a reason, as in normal use. |

## 4. Session (about 75 minutes each)
1. **5 min:** short reading on what the library does (same text for both groups).
2. **40 min:** the task. Save the chat log and the final code.
3. **5 min:** self-rating: "How well do you understand this library now?" 1–5, and "How much faster or slower was AI for you?"
4. **20 min:** the quiz, **without AI**. Docs allowed? Decide once and apply to both groups.
5. **Optional, stronger:** repeat the quiz (reordered) after 7 days, without notice. Delayed recall is the better measure of learning.

## 5. What to record per participant
- Group, task time, tests passed.
- Quiz score in total and per section (debugging, reading, concepts).
- Self-ratings.
- For the EMW group: modes chosen and any overrides with reasons (from `task-log.yaml`).
- Notes on friction: where EMW annoyed people or got skipped.

## 6. Grading
- Grade quizzes **without knowing the group** (strip names and shuffle before grading).
- Use the answer key written before the sessions.

## 7. Analysis
- Compare group averages and show every individual score; with this few people, the spread matters as much as the average.
- Report the debugging section separately (the largest gap in Anthropic's study).
- Report task time alongside quiz score: a slower group that learned more is a trade-off to state, not hide.
- Don't run significance tests and call them conclusive. Say "pilot, n = X".

## 8. Record the result, whatever it shows
- Fill in `pilot-results-template.md`.
- Add a shared knowledge entry, category `research`, status `proposed`, evidence type `direct-observation`, with the limitations (sample size, one library, one tool). A null or negative result is just as important to record.
- If friction notes show EMW steps being skipped, open issues for them. That is useful even if the scores show nothing.
