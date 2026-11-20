# EMW Learning Tracks

A track is a staged path for one language: what to learn, what to build, and when you may move on. The workflow is the coach and the record book; the track is the training plan.

## Files
| File | What it is |
|---|---|
| `core.yaml` | Skills shared by every track (Git, HTTP, SQL, testing, security and more), Stage 0, and the stage gate |
| `php.yaml` | The PHP track: modern PHP, then Laravel as the only framework |
| `briefs/` | One brief per stage project: the problem, what to build, edge cases, a "works when" checklist. No solution code |
| `briefs/php-house-rules.md` | Rules every PHP project follows |
| `track.schema.json` | The format of a track file |

Tracks for .NET, Go and Python are planned; see `docs/plans/learning-tracks-plan.md`.

## How a track is laid out
- **`skills`**: every skill the track teaches, with an id such as `php.pdo` or `laravel.eloquent`.
- **`stages`**: each has an outcome, a default collaboration mode, the skills it requires with a target level (M1–M4), one core project with a brief, and optional electives.
- **`extends: core`**: the track also uses the shared core skills, so a second language reuses what you have already proved.

## Starting a track by hand
A command to do this (`/emw-track`) is planned. Until then:
1. In your learning repository, run EMW onboarding (Prompt 01) so `.emw-project/` exists.
2. Copy the skills for your current stage from the track file into `.emw-project/skill-ledger.yaml`, each with `current_level: "M0"`, the stage's `target_level`, and `evidence: []`.
3. Open the stage brief and start. In Stages 0–2 use `/emw-practice`: you type, the agent hints.
4. Log tasks in `task-log.yaml` and evidence in `skill-ledger.yaml`. Run `python .emw/tools/emw_check.py`.
5. Move on when the gate in `core.yaml` is met.

## The stage gate
A stage is passed when the project is shipped, every listed skill is at its target, one piece was rebuilt from memory a week later, the stretch change was done with little or no AI help, and at least one check was seen by a human.

## Checking track files
`python .emw/tools/emw_check.py` validates every track: the format, that each stage's skills exist, that targets never go down between stages, and that every brief file is present.

## Adding a track
Copy `php.yaml`, change the id to match the new file name, keep `extends: core`, and write one brief per stage. Base the content on research with sources, as the PHP track is on `resources/research/`.
