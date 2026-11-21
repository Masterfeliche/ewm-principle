#!/usr/bin/env python3
"""emw_recall: show and record the recall checks a developer owes.

Usage (run from the developer's repository root):
    python .emw/tools/emw_recall.py due            # what is due or missed today
    python .emw/tools/emw_recall.py plan           # every skill's schedule, including upcoming
    python .emw/tools/emw_recall.py done <skill> --task "what you rebuilt from memory"

A recall check is a short piece of work done from memory, with no notes and no AI
beyond a conceptual hint: rebuild the piece, trace it, or fix a planted bug in it.
Research on spaced retrieval is the reason EMW schedules them instead of leaving
them to chance.

The clock starts at a skill's first dated evidence. Checks are due 2, 7 and 30 days
later by default; a team can change that with recall_days in .emw-project/mode-policy.yaml.
A check counts when an evidence item of type recall or rebuild, at assistance A0 or A1,
falls inside its window. `done` writes exactly such an item into
.emw-project/skill-ledger.yaml (the file is rewritten, so comments in it are not kept).

Exit code: 0 ok (nothing due for `due`), 1 something is due or missed, 2 could not run.
Requires PyYAML.
"""
from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    print("emw_recall: PyYAML is required. Install it with: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

sys.path.insert(0, str(Path(__file__).resolve().parent))
import emw_check  # noqa: E402

LABEL = {"done": "done", "due": "DUE", "missed": "missed", "upcoming": "upcoming"}


class RecallError(Exception):
    pass


def load_ledger(root: Path) -> tuple[Path, dict]:
    path = root / ".emw-project" / "skill-ledger.yaml"
    if not path.is_file():
        raise RecallError(f"no skill ledger at {path}. Run the onboarding prompt (01) "
                          "or start a track first.")
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise RecallError(f"cannot read {path}: {exc}") from exc
    if not isinstance(data, dict) or not isinstance(data.get("skills"), list):
        raise RecallError(f"{path} has no skills list")
    return path, data


def load_policy(root: Path) -> dict:
    rep = emw_check.Report()
    policy = emw_check.load_policy(root / ".emw-project" / "mode-policy.yaml", rep,
                                   root)
    for problem in rep.errors:
        print(f"WARN  {problem}", file=sys.stderr)
    return policy


def rows(root: Path, today: dt.date) -> list[tuple[dict, list[dict]]]:
    _, data = load_ledger(root)
    days = load_policy(root)["recall_days"]
    out = []
    for skill in data["skills"]:
        if not isinstance(skill, dict):
            continue
        slots = emw_check.recall_schedule(skill, today, days)
        if slots:
            out.append((skill, slots))
    return out


def print_slot(skill: dict, slot: dict) -> None:
    when = f"was due {slot['due']}" if slot["state"] in ("due", "missed") else f"due {slot['due']}"
    done_on = f" on {slot['on']}" if slot["on"] else ""
    print(f"  {LABEL[slot['state']]:<8} {slot['days']:>3}-day  {when}{done_on}   {skill.get('id')}")


def cmd_due(root: Path, args) -> int:
    today = args.date or dt.date.today()
    pending = []
    for skill, slots in rows(root, today):
        for slot in slots:
            if slot["state"] in ("due", "missed"):
                pending.append((skill, slot))
    if not pending:
        print(f"No recall check is due on {today}.")
        return 0
    print(f"Recall checks owed on {today}:")
    for skill, slot in pending:
        print_slot(skill, slot)
    print("\nFor each one: redo the piece from memory, with no notes and no AI beyond a "
          "conceptual hint.\nFollow .emw/prompts/13-recall.md, then record it:")
    print(f"  python .emw/tools/emw_recall.py done {pending[0][0].get('id')} "
          "--task \"what you rebuilt and what you got wrong\"")
    print("A missed check is not a failure. Do it now; the schedule restarts from "
          "the skill's first evidence, so later slots still apply.")
    return 1


def no_schedule_reason(root: Path) -> str:
    """Say which of the three causes left the schedule empty, rather than asserting one."""
    _, data = load_ledger(root)
    skills = [s for s in data["skills"] if isinstance(s, dict)]
    if not load_policy(root)["recall_days"]:
        return ("recall_days is [] in .emw-project/mode-policy.yaml, so no recall check "
                "is scheduled.")
    if not skills:
        return "The skill ledger has no skills yet, so no recall check is scheduled."
    return "No skill has dated evidence yet, so no recall check is scheduled."


def cmd_plan(root: Path, args) -> int:
    today = args.date or dt.date.today()
    table = rows(root, today)
    if not table:
        print(no_schedule_reason(root))
        return 0
    print(f"Recall schedule on {today} (clock starts at each skill's first evidence):")
    for skill, slots in table:
        print(f"{skill.get('id')}  ({skill.get('current_level')})")
        for slot in slots:
            print_slot(skill, slot)
    return 0


def cmd_done(root: Path, args) -> int:
    today = args.date or dt.date.today()
    path, data = load_ledger(root)
    skill = next((s for s in data["skills"] if isinstance(s, dict) and s.get("id") == args.skill), None)
    if skill is None:
        ids = ", ".join(str(s.get("id")) for s in data["skills"] if isinstance(s, dict))
        raise RecallError(f"no skill '{args.skill}' in the ledger. It has: {ids}")
    item = {"date": today.isoformat(), "type": "recall", "assistance": args.assistance,
            "verified_by": "self", "task": args.task}
    skill.setdefault("evidence", [])
    if not isinstance(skill["evidence"], list):
        raise RecallError(f"evidence on '{args.skill}' is not a list; fix the ledger by hand")
    skill["evidence"].append(item)
    text = yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=100)
    path.write_text(emw_check.ledger_header("Recall checks are appended by emw_recall.py.")
                    + text, encoding="utf-8")
    print(f"Recorded an {args.assistance} recall check on {args.skill} for {today}.")
    slots = emw_check.recall_schedule(skill, today, load_policy(root)["recall_days"])
    nxt = next((s for s in slots if s["state"] == "upcoming"), None)
    if nxt:
        print(f"Next check on this skill: {nxt['days']}-day, due {nxt['due']}.")
    elif slots:
        print("That was the last scheduled check for this skill.")
    else:
        print(no_schedule_reason(root))
    print("If the rebuild needed notes or AI help, lower the level in the ledger "
          "rather than leaving it as it is.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Show and record EMW recall checks.")
    parser.add_argument("--root", default=".", help="repository root (default: current directory)")
    sub = parser.add_subparsers(dest="command", required=True)
    p_due = sub.add_parser("due", help="checks that are due or missed today")
    p_plan = sub.add_parser("plan", help="every skill's schedule, including upcoming checks")
    p_done = sub.add_parser("done", help="record a recall check you have just finished")
    p_done.add_argument("skill", help="skill id from the ledger")
    p_done.add_argument("--task", required=True, help="what you rebuilt, and what you got wrong")
    p_done.add_argument("--assistance", default="A0", choices=["A0", "A1"],
                        help="A0 no help at all (default), A1 a conceptual hint")
    for p in (p_due, p_plan, p_done):
        p.add_argument("--date", type=dt.date.fromisoformat, help=argparse.SUPPRESS)
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    commands = {"due": cmd_due, "plan": cmd_plan, "done": cmd_done}
    try:
        return commands[args.command](root, args)
    except RecallError as exc:
        print(f"emw_recall: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
