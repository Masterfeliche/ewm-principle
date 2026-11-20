# EMW Learning Tracks

A track is a staged path for one language: what to learn, what to build, and when you may move on. The workflow is the coach and the record book; the track is the training plan.

## Files
| File | What it is |
|---|---|
| `core.yaml` | Skills shared by every track (Git, HTTP, SQL, testing, security and more), Stage 0, and the stage gate |
| `php.yaml` | The PHP track: modern PHP, then Laravel as the only framework |
| `briefs/` | One brief per stage project: the problem, what to build, edge cases, a "works when" checklist. No solution code |
| `briefs/house-rules.md` | Rules every track project follows |
| `track.schema.json` | The format of a track file |

Tracks for .NET, Go and Python are planned; see `docs/plans/learning-tracks-plan.md`.

## How a track is laid out
- **`skills`**: every skill the track teaches, with an id such as `php.pdo` or `laravel.eloquent`.
- **`stages`**: each has an outcome, a default collaboration mode, the skills it requires with a target level (M1–M4), one core project with a brief, and optional electives.
- **`extends: core`**: the track also uses the shared core skills, so a second language reuses what you have already proved.

## Following a track
In your learning repository (with `.emw/` installed), use `/emw-track` in Claude Code or OpenCode, or run the tool directly:

```bash
python .emw/tools/emw_track.py start php
```

```bash
python .emw/tools/emw_track.py status
```

```bash
python .emw/tools/emw_track.py ship --url https://github.com/you/your-project
```

```bash
python .emw/tools/emw_track.py next
```

- `start` creates `.emw-project/track.yaml` and adds the first stage's skills to your skill ledger at M0. A PHP learner starts at core Stage 0.
- `status` shows your stage, each skill against its target, the project brief and the gate checklist.
- `next` opens the next stage only when the gate is met; otherwise it lists what is missing.

Day to day: read the stage brief, build the project (in Stages 0–2 use `/emw-practice`: you type, the agent hints), and record evidence on each skill in `skill-ledger.yaml`:

```yaml
- date: "2026-12-03"
  type: "rebuild"        # implement | debug | modify | transfer | rebuild | explain ...
  assistance: "A0"       # A0 none ... A4 the AI wrote it
  verified_by: "self"    # "human" only when a mentor or peer saw it
  task: "Rebuilt the router from memory with tests"
```

The skill ledger is rewritten by the tool, so comments you add to it are not kept.

## The stage gate
`emw_track.py next` checks six things:

| Item | Met by |
|---|---|
| shipped | A project URL recorded with `ship --url` |
| levels | Every stage skill at its target level |
| human | One evidence item with low AI help (A0–A2) and `verified_by: human`, dated in this stage |
| rebuild | One `type: rebuild` item (A0–A2) dated at least 7 days after the stage began |
| transfer | One `type: transfer` item (A0–A1): the stretch change in the brief |
| check | `emw_check` passes |

Evidence from an earlier stage does not count toward a later gate. Reviews at 2 days, 1 week and 1 month are planned but not built.

## Checking track files
`python .emw/tools/emw_check.py` validates every track: the format, that each stage's skills exist, that targets never go down between stages, and that every brief file is present.

## Adding a track
Copy `php.yaml`, change the id to match the new file name, keep `extends: core`, and write one brief per stage. Base the content on research with sources, as the PHP track is on `resources/research/`.
