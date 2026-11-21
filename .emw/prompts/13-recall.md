# EMW Prompt 13 — Recall Check (From Memory)

Use when `python .emw/tools/emw_recall.py due` lists a check, when `emw_check` prints a recall note, or when the developer wants to find out whether something they built earlier has stuck.

**Principle:** memory is strengthened by retrieving it, not by seeing it again. Spacing those retrievals out over days keeps what re-reading does not. Rereading your own code feels like knowing it; rebuilding it from an empty file is what proves you do. A check that is partly wrong is still a successful check: the gap it shows is the thing worth working on next.

## Rules for the agent
1. **Give no code, no notes, and no file from the developer's earlier work** until they have finished their attempt and said so. Not a skeleton, not a signature, not a reminder of the function they used.
2. **Do not open their earlier implementation in front of them**, and do not quote it back. If they ask what they wrote last time, say it after the attempt.
3. One conceptual hint is allowed when they are fully stuck; that makes the check A1 rather than A0. A second hint, or any code, ends the check: record it as practice (Prompt 11), not as recall.
4. Keep it to 15–30 minutes. A recall check is small on purpose.
5. **Never record the result yourself as better than it was.** A rebuild that needed the old code is not a passed check.

## Session flow
1. **Name the piece.** Take the skill id from the `emw_recall.py due` output. Pick the smallest thing that shows the skill: the query layer, not the whole app; the middleware, not the framework.
2. **State the task from the outside only:** what it must do, its inputs and outputs, one edge case, and how they will know it works. No structure, no naming, no hints about approach.
3. **Developer writes it in an empty file,** with no notes, no earlier repository open, and no AI.
4. **They run it** against the success test they were given.
5. **Compare afterwards.** Now the earlier version can be opened. Ask them to name every difference and say which version is better and why. The differences are the real result of the check.
6. **Record it** (see below), and agree the one thing to do about the biggest gap.

## What the result means
| What happened | What to record | What to do next |
|---|---|---|
| Rebuilt it, worked, no help | `assistance: A0` | Keep the level. The next scheduled check still applies |
| Rebuilt it after one conceptual hint | `assistance: A1` | Keep the level, note the hint in `task` |
| Needed the old code, or could not start | Record it as A1 with an honest `task`, then **lower `current_level` by one** | Do a Prompt 11 practice session on that piece this week |
| Could not remember what it was for at all | Same, and lower the level | Treat the skill as new again |

Lowering a level is not a punishment and not a failure of the developer. A level that is not there cannot be relied on in planning, and an honest ledger is the only kind worth keeping.

## Record
```bash
python .emw/tools/emw_recall.py done <skill-id> --task "what you rebuilt, and what you got wrong"
```

That appends an evidence item of type `recall` at A0 (add `--assistance A1` when you gave a hint) and prints when the next check on that skill is due. Write the `task` line so it is useful in six months: "rebuilt the PDO wrapper; forgot to set ERRMODE_EXCEPTION and used string interpolation in one query" beats "went fine".

## Schedule
Checks are due 2, 7 and 30 days after a skill's first evidence. A team can change the days with `recall_days` in `.emw-project/mode-policy.yaml`, or set `[]` to turn them off. A missed check is reported until it is done; do it late rather than not at all, and let the remaining slots stand.
