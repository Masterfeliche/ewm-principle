# Using EMW End to End

A practical guide to the Engineering Mastery Workflow: for learning a language from zero, for working on a project that already exists, and for leading a team.

## 1. What EMW does

AI coding tools let you ship code you do not understand. EMW keeps the AI useful while making sure you can still do the work yourself. It does three things:

1. **Decides how much the AI does.** The less you have proved you know, the more you do yourself and the more the AI only coaches.
2. **Keeps two records, never one.** What was delivered, and what you can do without AI. Finishing a feature does not count as proof you learned it.
3. **Checks the records.** A small tool refuses claims that have no evidence.

The whole thing is files in your repository. Any coding agent that reads `AGENTS.md` can follow it.

### The three scales you will see everywhere

| Scale | Values | Meaning |
|---|---|---|
| **Mode** (how you work with the AI) | 1 | You reason and type; the AI asks questions and gives hints |
| | 2 | You plan together; you write the core logic; the AI helps and reviews |
| | 3 | The AI drafts; you audit it and show you understand it |
| | 4 | The AI does narrow, routine work you already know well |
| **Mastery level** (what you can do) | M0 | No evidence yet |
| | M1 | Can explain what it is for |
| | M2 | Can use it with hints, examples or AI help |
| | M3 | Can build, test, explain and debug it without solution-level help |
| | M4 | Can handle unfamiliar cases, compare alternatives and teach it |
| **Assistance** (how much help a piece of work had) | A0 | None beyond documentation |
| | A1 | A hint or explanation |
| | A2 | Pseudocode or a pointer to the right function |
| | A3 | The AI wrote part of it |
| | A4 | The AI wrote it |

Two rules tie them together. Work done at A3 or A4 never proves M3. And M3 or M4 needs at least one piece of low-help evidence that **a person** saw.

## 2. Set up

You need Python 3.9 or newer and PyYAML (`pip install pyyaml`).

Copy these from the EMW repository into the root of your own repository:

| Copy | Why |
|---|---|
| `.emw/` | The rules, prompts, templates, tracks and tools |
| `AGENTS.md` | The contract every agent reads first. If you already have one, merge the EMW text into it |
| `CLAUDE.md` and `.claude/` | For Claude Code: slash commands and skills |
| `opencode.json` and `.opencode/` | For OpenCode |
| `GEMINI.md`, `.cursor/rules/emw.mdc`, `.github/copilot-instructions.md` | For Gemini CLI, Cursor, Copilot (one pointer file each) |
| `.github/workflows/emw-check.yml` | Optional: runs the checker on every pull request |

Then check it works:

```bash
python .emw/tools/emw_check.py
```

Your own records never go inside `.emw/`. They live in two folders the workflow creates for you: `.emw-project/` (status and ledgers) and `.project-knowledge/` (lessons about this project).

## 3. Pick your path

| You are… | Go to |
|---|---|
| Learning a language from zero, or adding a second one | Section 4: learning with a track |
| Working on a real codebase and want to keep your skills | Section 5: an ongoing project |
| Leading a team or mentoring juniors | Section 6: teams |

You can do both 4 and 5. They use the same skill ledger.

## 4. Learning with a track

A track is a training plan for one language: six stages, a project for each, and a gate you must pass to move on. There are four: `php`, `dotnet`, `go`, `python`. All start with the same Stage 0.

| Stage | Ends with | Rough time at 10–15 hours a week |
|---|---|---|
| 0 Ground floor | A page online, a Git repository, first SQL queries | 2–4 weeks |
| 1 Language foundations | A tested command-line tool | 2–3 months |
| 2 Web and database | A small web app with login, deployed | 2–3 months |
| 3 Framework and professional habits | A deployed app or API with tests and CI | 3–6 months |
| 4 Production engineering | A system with background work, caching and monitoring | 6–12 months |
| 5 Systems and scale | A load-tested service and a performance report | ongoing |

The times are estimates. Nobody is behind.

### Step 1: start

Make a new repository for your learning, install EMW (section 2), then:

```bash
python .emw/tools/emw_track.py start php
```

In Claude Code or OpenCode you can type `/emw-track start php` instead. This creates your progress file and adds the Stage 0 skills to your skill ledger at M0.

### Step 2: see where you are

```bash
python .emw/tools/emw_track.py status
```

It shows your stage, each skill against its target, the project brief to read, and a checklist of what the gate still needs.

### Step 3: read the brief

Each stage has a brief in `.emw/tracks/briefs/`. It gives the problem, what to build, the edge cases you must handle, and a "works when" checklist. It contains no solution code. Read `house-rules.md` once too: money as whole shillings, Kiswahili and English, sandbox only, never hold other people's money.

### Step 4: build it, typing the code yourself

In Stages 0–2 the AI is a coach. Start a session with:

```
/emw-practice <the thing you are working on>
```

It sets a small task, asks what you expect to be hard, and gives one hint at a time: a question, then the concept, then pseudocode, then the name of a function to look up. It does not show a full solution before you have tried. If you insist, it will give the answer and the work is recorded as A4, which does not count toward your gate.

Why this way: what makes code stick is producing it from your own head. Reading or pasting an answer teaches very little.

### Step 5: record what you did

After each real piece of work, add an evidence item to that skill in `.emw-project/skill-ledger.yaml`:

```yaml
- date: "2026-12-03"
  type: "implement"      # implement | debug | modify | explain | transfer | rebuild
  assistance: "A1"
  verified_by: "self"    # "human" only when a mentor or peer saw it
  task: "Wrote the amount parser and its tests; needed one hint on regular expressions"
```

When the evidence supports it, raise `current_level`. The agent can help you write the entry and suggest a level. It must not invent evidence or mark anything as human-verified.

### Step 6: pass the gate

| The gate needs | How you meet it |
|---|---|
| shipped | `python .emw/tools/emw_track.py ship --url <repository or live address>` |
| levels | Every stage skill at its target |
| human | One low-help item (A0–A2) that a mentor or peer saw: `verified_by: human` |
| rebuild | The piece named in the brief, rebuilt from memory at least 7 days after the stage began: `type: rebuild` |
| transfer | The brief's stretch change, done at A0 or A1: `type: transfer` |
| check | `emw_check` passes |

Then:

```bash
python .emw/tools/emw_track.py next
```

If anything is missing it tells you what. If the gate is met it opens the next stage and adds its skills. Evidence from an earlier stage does not count again.

### What a week looks like

- **Most days:** work on the stage project with `/emw-practice`. Record evidence as you go.
- **Once a week:** run `/emw-weekly`. It lists what you practised, what is weak, and gives you one short exercise without AI.
- **Whenever `emw_recall.py due` lists something:** do that check from memory, with no notes and no earlier code open. It takes 15–30 minutes.
- **When the checker says a skill is due:** do a 10–20 minute check without AI: predict what code does, trace it, or fix a planted bug.

### Recall checks

Building something once does not make it yours. Two days later, a week later, and a month later, EMW asks you to rebuild a small part of it from memory — no notes, no old repository open, no AI beyond one conceptual hint.

```bash
python .emw/tools/emw_recall.py due     # what you owe today
python .emw/tools/emw_recall.py plan    # the whole schedule, including what is coming
```

Type `/emw-recall` and the agent will set the task from the outside only and keep your earlier code shut until you are done. When you finish, record it:

```bash
python .emw/tools/emw_recall.py done php.pdo --task "rebuilt the query layer; forgot the error mode"
```

The point is not to pass. If the rebuild needed the old code, the level in your ledger was not real — lower it by one and practise that piece this week. A check you missed is still worth doing late; the tool keeps listing it until you do.

The days are 2, 7 and 30 after a skill's first evidence. A team lead can change them with `recall_days` in `.emw-project/mode-policy.yaml`, or set `[]` to switch them off.

### Find a human

The gate will not open without a person. Arrange a mentor, a senior colleague, or a study partner on the same track before you start. Fifteen minutes of someone watching you explain or change your code is enough for one stage.

### A second language

The shared skills (Git, HTTP, SQL, testing, security, Docker, CI) carry over, so Stage 1 of a second track takes weeks, not months. One learner follows one track per repository; start the second in a new repository and copy the evidence for the shared `core.` skills across.

## 5. An ongoing project

Use this when you already have a codebase and real work to deliver.

### First session: onboard the project

Open the repository in your agent and run `/emw-onboard` (or ask it to follow `.emw/prompts/01-project-onboarding.md`). It reads the code and creates:

| File | What it holds |
|---|---|
| `.emw-project/project-profile.md` | What the product is, the stack, the architecture, the risks |
| `.emw-project/delivery-ledger.md` | Features, decisions, defects, checks run |
| `.emw-project/skill-ledger.yaml` | The skills this project needs, your level in each, and the evidence |
| `.emw-project/task-log.yaml` | One line per meaningful task: mode, assistance, skills |
| `.emw-project/mode-policy.yaml` | Your team's defaults for how much the AI does |
| `.project-knowledge/` | Lessons and rules specific to this project |

Levels start low on purpose. Raise them as you record evidence. Review the profile and correct anything the agent got wrong.

### Every task: one of two paths

**Quick path, for trivial work.** A change is trivial when it is about 30 lines or fewer, touches nothing high-risk (login, permissions, tenants, payments, secrets, personal data, destructive database changes, deployment), and only uses skills you already hold at M3. The agent just does it and reports three things: what it ran, what it did not run, and risks.

**Full path, for everything else.** Start with `/emw-feature <what you want>`. The agent then:

1. Looks up relevant knowledge from earlier work.
2. Reads the code and tests before proposing anything.
3. **Proposes a mode** from your mode policy and your level in the weakest skill involved. With the built-in policy, M0–M1 means Mode 1, M2 means Mode 2, M3 and above means any mode.
4. Agrees the plan with you: scope, what "done" means, edge cases, tests, and which parts you will own.
5. Builds in small steps, in that mode.
6. Verifies, and reports what was checked and what was not.
7. Updates the delivery ledger, adds a line to the task log, and records evidence on your skills.

### When you need speed

You can always pick a mode with less practice than the default. Say so, give the reason, and it is written into the task log as `mode_reason`:

```yaml
- id: "T-0042"
  date: "2026-12-03"
  summary: "Hotfix: invoice total rounding"
  mode: 4
  assistance: "A4"
  skills: ["backend.money"]
  mode_reason: "Production incident; will redo in Mode 2 as T-0043"
```

Without a reason the checker fails. With one it passes. The point is that skipping the learning is a decision someone made, not something that happened by default.

### The other commands

| Command | Use it when |
|---|---|
| `/emw-learn <technology>` | The task needs something you do not know yet |
| `/emw-debug <problem>` | Something is broken. You state a hypothesis before any code changes |
| `/emw-review` | A change, yours or the AI's, needs review |
| `/emw-capture <lesson>` | You found something worth remembering: a root cause, a rule, a trap |
| `/emw-weekly` | Once a week: progress, gaps, and one exercise without AI |
| `/emw-practice <skill>` | A skill is overdue for a check, or you want to learn by doing |
| `/emw-recall <skill>` | A recall check is due: rebuild it from memory, nothing open |

### Checks without AI

After a skill has been used in four logged tasks with no new low-help evidence, the checker warns that a check is due. Do a short one from `.emw/assessments/` or a practice session, and record it. This is how the ledger stays honest on a project where the AI writes a lot.

Recall checks run on their own clock, 2, 7 and 30 days after each skill's first evidence. They apply to ongoing projects exactly as they do to learning tracks: `python .emw/tools/emw_recall.py due` lists them, and the checker prints a due one as a `NOTE`, which never fails a build. On a busy delivery team, set `recall_days` in `mode-policy.yaml` to something you will actually do — `[7, 30]` is a reasonable start — rather than switching them off.

### High-risk work

Whatever the mode, a person approves and independently verifies anything touching login and permissions, tenant separation, payments, secrets, personal data, destructive database changes and production deployment. The AI may help. It is never the only checker.

### Knowledge that lasts

`/emw-capture` writes a short entry to `.project-knowledge/` with the problem, the cause, the fix, the evidence and the limits. The agent looks these up before the next meaningful task, so the same bug is not rediscovered. Entries are marked draft, proposed or verified, and only verified ones are treated as fact.

## 6. Teams

### Set the policy once

Edit `.emw-project/mode-policy.yaml`:

```yaml
default_mode_by_level:
  M0: 1
  M1: 1
  M2: 2
  M3: any
  M4: any
mode4_min_level: M3     # full delegation below this level needs a written reason
assessment_every: 4     # tasks per skill before a check without AI is due
```

Stricter for a team of juniors, looser for seniors in familiar code. The agent proposes modes from this file, so nobody has to police it by hand.

### Turn on the checker in CI

Copy `.github/workflows/emw-check.yml`. Every pull request then fails if the records are inconsistent: a Mode 4 task on a weak skill with no reason, an M3 claim with no human-verified evidence, a task naming a skill that does not exist.

### Be the human in the loop

A lead's main job in EMW is the one thing the AI cannot do: watch someone do the work and mark it `verified_by: human`. Fifteen minutes per person per fortnight covers most of it. Ask them to explain a piece of code, change it while you watch, or find a bug you planted.

### Read the records

| Look at | To learn |
|---|---|
| `task-log.yaml` | How much work each person does in each mode and at each assistance level, and how often defaults are overridden |
| `skill-ledger.yaml` | Who can do what without AI, and which claims are thinly supported |
| `emw_check` warnings | Which skills are overdue for a check |
| `/emw-weekly` | A summary of all three |

Use these to coach and to plan who works on what. Do not use them for performance reviews: people stop recording honestly the moment the ledger is used against them.

### Onboarding a junior

Start them on a track (section 4) for their first weeks, then move them to the real project (section 5) with the same skill ledger. The shared `core.` skills they proved on the track count on the project.

## 7. The files, in one place

| File | Who writes it | What it is for |
|---|---|---|
| `AGENTS.md` | EMW | The rules the agent follows |
| `.emw/core/` | EMW | Detailed rules: modes, lifecycle, mastery, verification, knowledge |
| `.emw/prompts/` | EMW | One prompt per kind of task |
| `.emw/tracks/` | EMW | Learning tracks and project briefs |
| `.emw/tools/emw_check.py` | EMW | Checks every record |
| `.emw/tools/emw_track.py` | EMW | Starts and follows a track |
| `.emw/tools/emw_recall.py` | EMW | Lists and records checks from memory |
| `.emw-project/skill-ledger.yaml` | You and the agent | Skills, levels, evidence |
| `.emw-project/task-log.yaml` | You and the agent | One line per meaningful task |
| `.emw-project/mode-policy.yaml` | Team lead | How much the AI does by default |
| `.emw-project/delivery-ledger.md` | You and the agent | What was built, decided and verified |
| `.emw-project/track.yaml` | `emw_track.py` | Your stage on a track. Never edit by hand |
| `.project-knowledge/` | You and the agent | Lessons about this project |

## 8. Command reference

| Slash command | Tool or prompt behind it |
|---|---|
| `/emw-onboard` | Prompt 01: set up records for a project |
| `/emw-feature` | Prompt 02: plan and build a change |
| `/emw-learn` | Prompt 03: learn a technology while building |
| `/emw-review` | Prompt 05: review a change |
| `/emw-debug` | Prompt 06: investigate a defect |
| `/emw-capture` | Prompt 08: save a verified lesson |
| `/emw-weekly` | Prompt 09: weekly progress and gaps |
| `/emw-practice` | Prompt 11: you type, the AI hints |
| `/emw-track` | Prompt 12 and `emw_track.py`: start, status, ship, next |
| `/emw-recall` | Prompt 13 and `emw_recall.py`: a check from memory |

Slash commands exist for Claude Code and OpenCode. In other agents, ask in words ("follow the EMW feature prompt for…") or paste the prompt file.

```bash
python .emw/tools/emw_check.py            # check all records
python .emw/tools/emw_check.py --strict   # also fail on warnings
python .emw/tools/emw_track.py status     # where you are on a track
python .emw/tools/emw_recall.py due       # checks from memory you owe today
python .emw/tools/emw_recall.py plan      # the whole recall schedule
```

## 9. Common mistakes

| Mistake | What to do instead |
|---|---|
| Asking for the solution "just this once" in Stages 0–2 | Ask for the next hint. If you take the answer, record A4 and rebuild it from memory later |
| Raising a level because the feature shipped | Raise it when there is evidence you did it with little help |
| Marking your own work `verified_by: human` | Only a person who saw it can be the human |
| Logging every tiny edit | Log meaningful tasks. Trivial work takes the quick path and is not logged |
| Editing `track.yaml` to get past a gate | Meet the gate. The file is the tool's, not yours |
| Using the ledger to judge people | Use it to coach and plan |
| Letting records go stale | Run `/emw-weekly`; fix what `emw_check` reports |
| Skipping recall checks because the code still looks familiar | Familiarity is not recall. Do the check in an empty file |

## 10. When the checker complains

| Message | Meaning | Fix |
|---|---|---|
| `current_level M2 has no evidence` | A level was set with nothing behind it | Add evidence, or set the level back to M0 |
| `M3 needs at least one evidence item with assistance A0-A2` | All the evidence was AI-heavy | Do one piece of the work with little help and record it |
| `M3 needs an A0-A2 evidence item with verified_by: human` | Nobody saw it | Ask a mentor or peer to watch, then record it |
| `mode 4 gives less support than the policy default` | Work was delegated on a weak skill | Add `mode_reason`, or redo it in the default mode |
| `skill 'x' is not in skill-ledger.yaml` | The task log names an unknown skill | Add the skill to the ledger or fix the id |
| `used in 4 tasks … run a short check without AI` | A check is due (a warning) | Do a 10–20 minute check and record it |
| `2-day recall check is due` | A check from memory is owed (a note, never a failure) | Run `/emw-recall`, then `emw_recall.py done` |
| `recall_days … must be a list of whole days in rising order` | `mode-policy.yaml` has a bad schedule | Use something like `[2, 7, 30]`, or `[]` to switch them off |
| `entry is not listed in index.yaml` | A knowledge file is missing from the index | Add it to the index |

## 11. Limits to know

- **EMW is instructions, not enforcement.** The checker validates records. It cannot see whether an agent really withheld a solution. That depends on the agent and on you.
- **Its own effect is not measured yet.** It is built on research into AI and learning, and a method for a small trial is in `docs/research/pilot.md`, but no trial has been run.
- **Scheduled recall checks are reminders, not proof.** The tool schedules them and records what you say happened. Nothing stops you recording a check you did with the old file open; only you lose by it.
- **The track tool rewrites `skill-ledger.yaml`,** so comments you add to that file are lost.
- **Track projects use sandboxes and invented data only.** Real payments, real SMS sender names, real tax receipts and real people's data need a registered business and, for some activities, a licence. See `resources/research/`.
