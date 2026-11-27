#!/usr/bin/env python3
"""emw_track: start and follow an EMW learning track.

Usage (run from the learner's repository root):
    python .emw/tools/emw_track.py start php       # begin a track at its first stage
    python .emw/tools/emw_track.py status          # where you are, and what the gate still needs
    python .emw/tools/emw_track.py ship --url URL  # record where the stage project lives
    python .emw/tools/emw_track.py next            # pass the gate and open the next stage

State lives in .emw-project/track.yaml. Skills are added to .emw-project/skill-ledger.yaml
(the file is rewritten, so comments in it are not kept).

The gate for a stage (from .emw/tracks/core.yaml) is checked as:
  shipped   the stage has a project URL (see `ship`)
  levels    every stage skill is at or above its target level
  human     an A0-A2 evidence item with verified_by: human, dated in this stage
  rebuild   an A0-A2 evidence item of type rebuild or recall, dated 7+ days after the stage began
  transfer  an A0-A1 evidence item of type transfer, dated in this stage
  check     emw_check passes

Exit code: 0 ok, 1 gate not met or problems found, 2 could not run.
Requires PyYAML.
"""
from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import io
import shutil
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    print("emw_track: PyYAML is required. Install it with: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

sys.path.insert(0, str(Path(__file__).resolve().parent))
import emw_check  # noqa: E402

LEVELS = ["M0", "M1", "M2", "M3", "M4"]
REBUILD_GAP_DAYS = 7


class TrackError(Exception):
    pass


# --- loading --------------------------------------------------------------------

def load(path: Path):
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise TrackError(f"cannot read {path}: {exc}") from exc


def dump(path: Path, data, header: str = "") -> None:
    text = yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=100)
    path.write_text(header + text, encoding="utf-8")


def load_track(root: Path, track_id: str) -> dict:
    """Return {title, stages: [..in order..], skills: {id: definition}} with the parent merged in."""
    tracks_dir = root / ".emw" / "tracks"
    path = tracks_dir / f"{track_id}.yaml"
    if not path.is_file():
        have = sorted(p.stem for p in tracks_dir.glob("*.yaml")) if tracks_dir.is_dir() else []
        raise TrackError(f"no track '{track_id}' in .emw/tracks/ (found: {', '.join(have) or 'none'})")
    data = load(path)
    skills = {s["id"]: s for s in data.get("skills") or []}
    stages = [dict(s, track=track_id) for s in data.get("stages") or []]
    gate = data.get("gate") or []
    parent = data.get("extends")
    if parent:
        base = load_track(root, parent)
        skills = {**base["skills"], **skills}
        stages = base["stages"] + stages
        gate = gate or base["gate"]
    numbers = [s["number"] for s in stages]
    if len(set(numbers)) != len(numbers):
        raise TrackError(f"stage numbers {numbers} overlap between '{track_id}' and the track it extends")
    stages.sort(key=lambda s: s["number"])
    return {"id": track_id, "title": data.get("title", track_id), "stages": stages,
            "skills": skills, "gate": gate}


def as_date(value) -> dt.date | None:
    if isinstance(value, dt.datetime):
        return value.date()
    if isinstance(value, dt.date):
        return value
    try:
        return dt.date.fromisoformat(str(value))
    except ValueError:
        return None


# --- project files ----------------------------------------------------------------

class Project:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.dir = root / ".emw-project"
        self.state_path = self.dir / "track.yaml"
        self.ledger_path = self.dir / "skill-ledger.yaml"

    def state(self) -> dict:
        if not self.state_path.is_file():
            raise TrackError("no track started here. Run: python .emw/tools/emw_track.py start <track>")
        return load(self.state_path)

    def save_state(self, state: dict) -> None:
        dump(self.state_path, state, "# EMW learning track progress. Written by emw_track.py.\n")

    def ledger(self) -> dict:
        if self.ledger_path.is_file():
            data = load(self.ledger_path) or {}
        else:
            data = {}
        data.setdefault("version", 1)
        data.setdefault("skills", [])
        return data

    def save_ledger(self, ledger: dict) -> None:
        dump(self.ledger_path, ledger,
             emw_check.ledger_header("Skills were added by emw_track.py."))


def add_stage_skills(ledger: dict, track: dict, stage: dict) -> list[str]:
    """Add the stage's skills to the ledger, or raise the target of ones already there."""
    by_id = {s.get("id"): s for s in ledger["skills"] if isinstance(s, dict)}
    # drop the template's example node the first time a track adds skills
    ledger["skills"] = [s for s in ledger["skills"]
                        if not (isinstance(s, dict) and str(s.get("id", "")).startswith("example."))]
    changed = []
    for item in stage.get("skills") or []:
        sid, target = item["id"], item["target"]
        definition = track["skills"].get(sid, {})
        node = by_id.get(sid)
        if node is None:
            ledger["skills"].append({
                "id": sid,
                "name": definition.get("name", sid),
                "technology": track["title"] if not sid.startswith("core.") else "Shared core",
                "scope": definition.get("scope", "S1"),
                "prerequisites": [],
                "target_level": target,
                "current_level": "M0",
                "confidence": "low",
                "evidence": [],
                "last_assessed": None,
                "next_assessment": definition.get("covers", ""),
            })
            changed.append(f"added {sid} (target {target})")
        elif LEVELS.index(target) > LEVELS.index(node.get("target_level", "M0")):
            node["target_level"] = target
            changed.append(f"raised {sid} target to {target}")
    return changed


# --- gate ---------------------------------------------------------------------------

def check_detail(code: int, tail: str) -> str:
    """Explain a ticked check row that still mentions warnings.

    The gate runs emw_check without --strict on purpose: warnings mean records are
    incomplete, which should not stop an early-stage learner who has no product to profile
    yet. Without this note the row reads as a contradiction.
    """
    if code == 0 and " 0 warnings" not in tail and "warning" in tail:
        return tail + "  (warnings do not block the gate; run emw_check to see them)"
    return tail


def gate_report(project: Project, track: dict, state: dict) -> tuple[list[tuple[str, bool, str]], dict]:
    """Return ([(name, met, detail)], stage) for the current stage."""
    number = state["current_stage"]
    stage = next((s for s in track["stages"] if s["number"] == number), None)
    if stage is None:
        raise TrackError(f"stage {number} is not in track '{track['id']}'")
    record = next((r for r in state["stages"] if r["number"] == number), {})
    began = as_date(record.get("started_at")) or dt.date.min
    ledger = {s.get("id"): s for s in project.ledger()["skills"] if isinstance(s, dict)}

    behind, evidence = [], []
    for item in stage.get("skills") or []:
        node = ledger.get(item["id"])
        level = (node or {}).get("current_level", "M0")
        if level not in LEVELS or LEVELS.index(level) < LEVELS.index(item["target"]):
            behind.append(f"{item['id']} {level}->{item['target']}")
        for e in (node or {}).get("evidence") or []:
            if isinstance(e, dict) and (as_date(e.get("date")) or dt.date.min) >= began:
                evidence.append(e)

    def low_help(e, levels=("A0", "A1", "A2")):
        return e.get("assistance") in levels

    human = [e for e in evidence if low_help(e) and e.get("verified_by") == "human"]
    rebuild_from = began + dt.timedelta(days=REBUILD_GAP_DAYS) if began != dt.date.min else began
    # emw_recall.py records a from-memory rebuild as type: recall. Both words mean the
    # same evidence here, so the gate accepts either (emw_check.RECALL_TYPES).
    rebuild = [e for e in evidence if e.get("type") in emw_check.RECALL_TYPES and low_help(e)
               and as_date(e.get("date")) >= rebuild_from]
    transfer = [e for e in evidence if e.get("type") == "transfer" and low_help(e, ("A0", "A1"))]

    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        check_code = emw_check.main(["--root", str(project.root)])
    check_tail = out.getvalue().strip().splitlines()[-1] if out.getvalue().strip() else ""

    url = str(record.get("project_url") or "").strip()
    report = [
        ("shipped", bool(url), url or "no project URL recorded; run: emw_track.py ship --url <repo or live URL>"),
        ("levels", not behind, "all stage skills at target" if not behind else "behind: " + ", ".join(behind)),
        ("human", bool(human), f"{len(human)} human-verified A0-A2 item(s)" if human
         else "no A0-A2 evidence with verified_by: human in this stage"),
        ("rebuild", bool(rebuild), f"{len(rebuild)} rebuild item(s)" if rebuild
         else f"no A0-A2 evidence of type rebuild or recall dated on or after {rebuild_from}"),
        ("transfer", bool(transfer), f"{len(transfer)} transfer item(s)" if transfer
         else "no A0-A1 evidence of type transfer in this stage"),
        ("check", check_code == 0, check_detail(check_code, check_tail)),
    ]
    return report, stage


# --- commands --------------------------------------------------------------------------

def cmd_start(root: Path, args) -> int:
    project = Project(root)
    if project.state_path.exists():
        current = load(project.state_path)
        raise TrackError(f"track '{current.get('track')}' is already started here (stage "
                         f"{current.get('current_stage')}). Use status or next.")
    track = load_track(root, args.track)
    if not track["stages"]:
        raise TrackError(f"track '{args.track}' has no stages")
    project.dir.mkdir(exist_ok=True)
    templates = root / ".emw" / "templates"
    # Seed the skill ledger from the template so it keeps the template's shape; its
    # example skill is dropped by add_stage_skills below. onboarding-status.yaml is
    # deliberately not written here: starting a track does not onboard a project, and
    # a file saying "not-started" only makes an un-onboarded project look set up.
    for name in ("skill-ledger.yaml", "task-log.yaml", "mode-policy.yaml"):
        if not (project.dir / name).exists() and (templates / name).is_file():
            shutil.copy(templates / name, project.dir / name)

    first = track["stages"][0]
    today = args.date or dt.date.today()
    state = {"version": 1, "track": args.track, "started_at": str(today),
             "current_stage": first["number"],
             "stages": [{"number": first["number"], "name": first["name"], "started_at": str(today),
                         "project_url": "", "passed_at": None}]}
    ledger = project.ledger()
    # setdefault is not enough: the template seeds project with an empty string.
    if not ledger.get("project"):
        ledger["project"] = f"{track['title']} learning track"
    changed = add_stage_skills(ledger, track, first)
    project.save_ledger(ledger)
    project.save_state(state)
    print(f"Started track '{args.track}' ({track['title']}) at stage {first['number']}: {first['name']}.")
    for line in changed:
        print(f"  {line}")
    print(f"Project brief: .emw/tracks/{first['project']['brief']}")
    print("Next: read the brief, then run: python .emw/tools/emw_track.py status")
    if not (project.dir / "onboarding-status.yaml").exists():
        print("This project is not onboarded yet. Run /emw-onboard before feature work.")
    return 0


def cmd_status(root: Path, args) -> int:
    project = Project(root)
    state = project.state()
    track = load_track(root, state["track"])
    if state.get("completed_at"):
        print(f"Track '{state['track']}' completed on {state['completed_at']}.")
        return 0
    report, stage = gate_report(project, track, state)
    total = len(track["stages"])
    position = [s["number"] for s in track["stages"]].index(stage["number"]) + 1
    print(f"Track: {track['title']} ({state['track']})   Stage {stage['number']}: {stage['name']}"
          f"   ({position} of {total})")
    print(f"Outcome: {stage['outcome']}")
    print(f"Project: {stage['project']['title']}  ->  .emw/tracks/{stage['project']['brief']}")
    if stage.get("lessons"):
        print(f"Lessons: .emw/tracks/{stage['lessons']}")
    print(f"Default mode: {stage['default_mode']}   Time: {stage.get('duration_estimate', 'not estimated')}")
    ledger = {s.get("id"): s for s in project.ledger()["skills"] if isinstance(s, dict)}
    print("Skills (current -> target):")
    for item in stage.get("skills") or []:
        level = (ledger.get(item["id"]) or {}).get("current_level", "M0")
        ok = level in LEVELS and LEVELS.index(level) >= LEVELS.index(item["target"])
        name = track["skills"].get(item["id"], {}).get("name", "")
        print(f"  [{'x' if ok else ' '}] {item['id']:<30} {level} -> {item['target']}   {name}")
    print("Gate:")
    for name, met, detail in report:
        print(f"  [{'x' if met else ' '}] {name:<9} {detail}")
    if stage.get("electives"):
        print("Electives: " + "; ".join(e["title"] + (" (learn only)" if e.get("learn_only") else "")
                                         for e in stage["electives"]))
    met = all(m for _, m, _ in report)
    print("Gate met. Run: python .emw/tools/emw_track.py next" if met
          else "Gate not met yet. The unchecked items above are what is left.")
    return 0


def cmd_ship(root: Path, args) -> int:
    project = Project(root)
    state = project.state()
    record = next(r for r in state["stages"] if r["number"] == state["current_stage"])
    record["project_url"] = args.url
    project.save_state(state)
    print(f"Recorded project URL for stage {state['current_stage']}: {args.url}")
    return 0


def cmd_log(root: Path, args) -> int:
    """Append one evidence item to a skill.

    Hand-editing YAML is the step most likely to be skipped, and a ledger with gaps is
    worse than none: the developer plans around skills they never showed. This makes it
    one command. It deliberately does not change current_level -- promotion is the
    developer's decision against the guidance in .emw/core/mastery-framework.md.
    """
    project = Project(root)
    ledger = project.ledger()
    skill = next((s for s in ledger["skills"]
                  if isinstance(s, dict) and s.get("id") == args.skill), None)
    if skill is None:
        known = ", ".join(str(s.get("id")) for s in ledger["skills"] if isinstance(s, dict))
        raise TrackError(f"no skill '{args.skill}' in the ledger. It has: {known or 'none'}")
    if args.type not in emw_check.EVIDENCE_TYPES:
        raise TrackError(f"type '{args.type}' is not one of "
                         f"{', '.join(emw_check.EVIDENCE_TYPES)}")
    if args.assistance not in emw_check.ASSISTANCE:
        raise TrackError(f"assistance '{args.assistance}' is not one of "
                         f"{', '.join(emw_check.ASSISTANCE)}")
    if not args.task.strip():
        raise TrackError("--task cannot be empty; write what you did and what you got wrong")
    if args.verified_by == "human" and not (args.reviewer or "").strip():
        raise TrackError("--verified-by human needs --reviewer '<who saw the work>'. "
                         "Only the developer records this, after a real person reviewed it; "
                         "an agent must never mark its own review as human-verified.")

    item = {"date": (args.date or dt.date.today()).isoformat(),
            "type": args.type, "assistance": args.assistance,
            "verified_by": args.verified_by, "task": args.task.strip()}
    if args.reviewer:
        item["reviewer"] = args.reviewer.strip()
    evidence = skill.setdefault("evidence", [])
    if not isinstance(evidence, list):
        raise TrackError(f"evidence on '{args.skill}' is not a list; fix the ledger by hand")
    evidence.append(item)
    project.save_ledger(ledger)

    print(f"Recorded {args.assistance} {args.type} evidence on {args.skill} for {item['date']}.")
    if args.assistance in ("A3", "A4"):
        print("A3 and A4 show the work was done with the AI, not independently. They are "
              "worth recording and they do not count toward a stage gate.")
    print(f"{args.skill} is at {skill.get('current_level')}, unchanged. Raise a level only "
          "when the evidence meets .emw/core/mastery-framework.md, and decide that yourself.")
    return 0


def cmd_next(root: Path, args) -> int:
    project = Project(root)
    state = project.state()
    if state.get("completed_at"):
        print(f"Track '{state['track']}' is already complete.")
        return 0
    track = load_track(root, state["track"])
    report, stage = gate_report(project, track, state)
    missing = [(n, d) for n, met, d in report if not met]
    if missing:
        print(f"Stage {stage['number']} gate is not met:")
        for name, detail in missing:
            print(f"  [ ] {name:<9} {detail}")
        return 1
    today = args.date or dt.date.today()
    record = next(r for r in state["stages"] if r["number"] == stage["number"])
    record["passed_at"] = str(today)
    later = [s for s in track["stages"] if s["number"] > stage["number"]]
    if not later:
        state["completed_at"] = str(today)
        project.save_state(state)
        print(f"Stage {stage['number']} passed. Track '{state['track']}' complete.")
        return 0
    nxt = later[0]
    state["current_stage"] = nxt["number"]
    state["stages"].append({"number": nxt["number"], "name": nxt["name"], "started_at": str(today),
                            "project_url": "", "passed_at": None})
    ledger = project.ledger()
    changed = add_stage_skills(ledger, track, nxt)
    project.save_ledger(ledger)
    project.save_state(state)
    print(f"Stage {stage['number']} passed. Now on stage {nxt['number']}: {nxt['name']}.")
    for line in changed:
        print(f"  {line}")
    print(f"Project brief: .emw/tracks/{nxt['project']['brief']}")
    if nxt.get("lessons"):
        print(f"Lessons: .emw/tracks/{nxt['lessons']} (start with lesson 1)")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Start and follow an EMW learning track.")
    parser.add_argument("--root", default=".", help="repository root (default: current directory)")
    sub = parser.add_subparsers(dest="command")
    p_start = sub.add_parser("start", help="begin a track")
    p_start.add_argument("track")
    p_start.add_argument("--date", type=dt.date.fromisoformat, help=argparse.SUPPRESS)
    sub.add_parser("status", help="show the current stage and gate")
    p_ship = sub.add_parser("ship", help="record the stage project's URL")
    p_ship.add_argument("--url", required=True)
    p_log = sub.add_parser("log", help="record one evidence item on a skill")
    p_log.add_argument("skill", help="a skill id from .emw-project/skill-ledger.yaml")
    p_log.add_argument("--type", required=True,
                       help="|".join(emw_check.EVIDENCE_TYPES))
    p_log.add_argument("--assistance", required=True,
                       help="A0 independent ... A4 AI-authored")
    p_log.add_argument("--task", required=True, help="what you did, and what you got wrong")
    p_log.add_argument("--verified-by", dest="verified_by", default="self",
                       choices=["self", "human"],
                       help="human only after a real person reviewed the work")
    p_log.add_argument("--reviewer", help="who reviewed it; required with --verified-by human")
    p_log.add_argument("--date", type=dt.date.fromisoformat, help=argparse.SUPPRESS)
    p_next = sub.add_parser("next", help="pass the gate and open the next stage")
    p_next.add_argument("--date", type=dt.date.fromisoformat, help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    commands = {"start": cmd_start, "status": cmd_status, "ship": cmd_ship,
                "log": cmd_log, "next": cmd_next}
    try:
        return commands[args.command or "status"](root, args)
    except TrackError as exc:
        print(f"emw_track: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
