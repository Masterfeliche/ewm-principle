# EMW Prompt 12 — Learning Track

Use when the developer is following a learning track (`.emw-project/track.yaml` exists), wants to start one, or asks where they are, what is next, or whether they can move on.

A track is a staged path for one language: skills with target levels, one project per stage, and a gate. Track files are in `.emw/tracks/`; the tool is `.emw/tools/emw_track.py`.

## Commands
- `python .emw/tools/emw_track.py start <track>`: begin a track. Creates `.emw-project/track.yaml` and adds the first stage's skills to the skill ledger at M0.
- `python .emw/tools/emw_track.py status`: current stage, skills against targets, the project brief, and the gate checklist.
- `python .emw/tools/emw_track.py ship --url <url>`: record where the stage project lives.
- `python .emw/tools/emw_track.py next`: pass the gate and open the next stage. It refuses, and lists what is missing, if the gate is not met.

## What the agent does
1. Run `status` and report it in plain words: the stage, the project, what is done, what is left.
2. Read the stage's project brief, and from Stage 1 on also `briefs/house-rules.md` (it applies to the projects that ship software, not to Stage 0). The brief is the specification. Do not add requirements and do not drop any.
3. If the stage lists `lessons` in its track file, teach from them: start with the first lesson the developer has not finished, and follow the "For the agent" section of that stage's lessons README. Lessons come before the project; the project grows from the lessons' project steps. Worked examples in a lesson file may be shown in the chat, because they solve a different problem from the exercises. Everything the developer writes still follows Prompt 11.
4. Follow the stage's default mode. In Stages 0–2 that is Mode 1: use Prompt 11 (Practice). The developer types the code; give hints one step at a time and no complete solution before an attempt. A brief contains no solution code, and neither should you.
5. After each meaningful piece of work, help the developer record it: one entry in `task-log.yaml`, and an evidence item on the relevant skill in `skill-ledger.yaml` with the date, type, honest assistance level and `verified_by`.
6. Propose a level change only when the evidence meets the promotion guidance in `.emw/core/mastery-framework.md`. The developer decides.
7. When the developer asks to move on, run `next`. If it refuses, explain each missing item and how to meet it. Never edit `track.yaml` by hand to get past a gate.

## Gate items and how they are met
| Item | Met by |
|---|---|
| shipped | `ship --url` with the repository or live address |
| levels | every stage skill at its target in the skill ledger |
| human | one A0–A2 evidence item with `verified_by: human`: a mentor or peer saw the work. The agent is not a human reviewer |
| rebuild | one A0–A2 item with `type: rebuild` or `type: recall`, dated at least 7 days after the stage began: the piece named in the brief, rebuilt from memory. A check recorded with `emw_recall.py done` (Prompt 13) counts |
| transfer | one A0–A1 item with `type: transfer`: the stretch change in the brief |
| check | `python .emw/tools/emw_check.py` passes |

## Honesty rules
- Never record evidence for work the developer did not do, and never mark `verified_by: human` yourself.
- If the developer asked for and received the solution, the assistance level is A4 and it does not count toward the gate.
- Time estimates in a track are estimates. Do not tell the developer they are behind.
