# Your first session

For someone who has just installed EMW and wants to start learning. It covers the first
half hour and nothing else. When you reach the end, [the end-to-end guide](GUIDE.md) has
the rest: what a week looks like, recall checks, gates, and working on a real codebase.

If you have not installed EMW yet, do [that](INSTALLATION.md) first, in a new empty
repository you will use for learning.

## What you are agreeing to

EMW is not a tutor that writes code for you. It is closer to a colleague who will not
let you watch over their shoulder, because watching does not teach you much.

Three things follow from that, and they surprise people:

- **The agent will refuse to write code you are supposed to be learning.** Not out of
  strictness: a skill you have never typed is recorded as M0, and at M0 the workflow
  puts you in Mode 1, where you write the core logic and the agent asks questions,
  explains concepts and reviews what you wrote.
- **You can override it, and it costs you.** Ask outright for the solution and you will
  get it — recorded as assistance level A4, which does not count toward passing a stage.
  Nobody is stopping you. The ledger just stays honest about it.
- **The record is only worth what you put in it.** You will be asked to rebuild things
  from memory and to admit when the rebuild needed the old code. A ledger you flattered
  is worse than no ledger, because you will plan around a skill you do not have.

If that sounds like the wrong trade for you, it probably is, and that is fine — EMW is
aimed at people who want the ability, not just the working code.

## The first half hour

### 1. Start a track (2 minutes)

Four are available: `php`, `dotnet`, `go`, `python`. Each track starts at Stage 1 —
straight into your language.

```bash
python .emw/tools/emw_track.py start php
```

In Claude Code or OpenCode, `/emw-track start php` does the same thing. You should see:

```
Started track 'php' (PHP with Laravel) at stage 1: Language foundations.
  added core.terminal (target M2)
  added core.git (target M3)
  added php.syntax-types (target M3)
  ...
Project brief: .emw/tracks/briefs/php-stage-1.md
Next: read the brief, then run: python .emw/tools/emw_track.py status
This project is not onboarded yet. Run /emw-onboard before feature work.
```

Several skills, all at M0, because you have not shown this workflow anything yet. M0 means
"unknown", not "bad".

### 2. Onboard the project (5 minutes)

That last line matters. Starting a track is not the same as setting the project up.
Run the checker and it will tell you exactly what is missing:

```bash
python .emw/tools/emw_check.py
```

```
WARN  .emw-project: onboarding-status.yaml missing; run the onboarding prompt (01)
WARN  .emw-project/project-profile.md: required onboarding record is missing; run the onboarding prompt (01)
WARN  .emw-project/delivery-ledger.md: required onboarding record is missing; run the onboarding prompt (01)
WARN  .project-knowledge/README.md: required onboarding record is missing; run the onboarding prompt (01)
WARN  .project-knowledge/index.yaml: required onboarding record is missing; run the onboarding prompt (01)
emw_check: shared knowledge + project records + 5 tracks; 4 shared entries; 0 errors, 5 warnings
```

**This is not a failure.** Warnings are a to-do list; the exit code is still 0. Type:

```
/emw-onboard
```

and the agent fills those records in. In a fresh learning repository most of the project
profile will say "nothing yet", because there is no application to describe — that is
the correct answer, not a gap. It takes a few minutes. Run the checker again and the
warnings should be gone.

### 3. See where you stand (1 minute)

```bash
python .emw/tools/emw_track.py status
```

The bottom half is the gate — what Stage 1 needs before it opens Stage 2:

```
Gate:
  [ ] shipped   no project URL recorded; run: emw_track.py ship --url <repo or live URL>
  [ ] levels    behind: php.syntax-types M0->M3, php.arrays-functions M0->M3, ...
  [ ] human     no A0-A2 evidence with verified_by: human in this stage
  [ ] rebuild   no A0-A2 evidence of type rebuild or recall dated on or after ...
  [ ] transfer  no A0-A1 evidence of type transfer in this stage
  [x] check     emw_check: ... 0 errors, 0 warnings
```

Everything unchecked on day one is normal. Two of these are worth reading now rather
than discovering in six weeks:

- **human** needs a real person — a mentor, a senior colleague, or someone else on a
  track — to watch you explain or change your own code, for about fifteen minutes.
  Arrange that early. The gate will not open without it, and you cannot sign it yourself.
- **rebuild** cannot be met in the first week. It wants the thing named in your brief,
  rebuilt from memory, **at least seven days** after you started the stage. That waiting
  period is the point: it is testing what stuck, not what you can copy.

### 4. Read the brief (10 minutes)

```bash
cat .emw/tracks/briefs/php-stage-1.md
```

Stage 1 asks for a tested command-line tool that reads messy real-world input. The
brief is the specification — it contains no solution code, and neither should the agent.
Read the "It works when" checklist before you start building, not after.

**Then open the lessons.** The brief says *what* to build; the lessons teach you *how*, in
order, starting from zero: `.emw/tracks/lessons/php-stage-1/README.md` for PHP Stage 1.
Lesson 1 covers the terminal and installing PHP — no prior experience required. Ask the
agent to "start lesson 1" and it will teach from them.

### 5. Start working (the rest of your life)

```
/emw-practice writing my first PHP function
```

The agent sets a small task, asks what you think will be hard, and then gives one hint
at a time: a question first, then the concept, then pseudocode, then the name of a
function to look up. You type everything.

When you finish something real, record it — one entry against the skill in
`.emw-project/skill-ledger.yaml`. The agent can write the entry with you. Be accurate
about `assistance`; it is the only field that can lie.

## Where to go next

- **[The end-to-end guide](GUIDE.md)**, section 4: the weekly rhythm, recall checks,
  evidence, and passing the gate.
- `python .emw/tools/emw_recall.py due` — nothing yet, because checks are scheduled from
  your first dated evidence. Expect it to start asking a couple of days after you record
  something.
- `/emw-weekly` — run it at the end of your first week.

## If something looks wrong

| What you see | What it means |
|---|---|
| Warnings from `emw_check` | A to-do list, not an error. Exit code 0. Errors are the ones to fix |
| `[x] check` next to a line mentioning warnings | The gate counts errors, not warnings. Run the checker separately to see them |
| "No recall check is due" | Correct until a skill has dated evidence. Record some work first |
| The agent will not write your code | Working as intended at M0. Ask for a hint, or say plainly that you want the solution and accept the A4 |
| `emw_track.py next` refuses | It lists what is missing. Nothing is hidden; work through the list |

## One honest caveat

EMW is new. The tooling has been tested; whether the method actually produces stronger
engineers has not been measured yet — see the [pilot study method](research/pilot.md).
You are early. If something is confusing or wrong, that is worth reporting rather than
working around.
