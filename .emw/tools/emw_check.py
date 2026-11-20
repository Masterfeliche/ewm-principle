#!/usr/bin/env python3
"""emw_check: validate EMW knowledge and project records.

Usage:
    python .emw/tools/emw_check.py                 # check the repo in the current directory
    python .emw/tools/emw_check.py --root path/to/repo
    python .emw/tools/emw_check.py --strict        # treat warnings as errors

What it checks:
  Shared knowledge (.emw/knowledge/)
    - index.yaml matches knowledge-index.schema.json
    - every indexed path exists, ids are unique, index metadata agrees with the entry
    - every entry's frontmatter matches knowledge-entry.schema.json
    - every entry file is listed in the index
    - status rules: verified needs non-reasoned evidence; superseded needs superseded_by
  Learning tracks (.emw/tracks/*.yaml, when present)
    - each track matches track.schema.json
    - 'extends' resolves; stage numbers are unique and in order
    - every stage skill is defined in the track or the track it extends
    - a skill's target level never goes down from one stage to the next
    - every project brief file exists; unused skills are reported
  Project records (only when .emw-project/ or .project-knowledge/ exist)
    - onboarding-status.yaml status and referenced files
    - skill-ledger.yaml levels, and M3/M4 claims backed by evidence
    - task-log.yaml fields, skill ids, and the team mode policy
      (mode-policy.yaml, or built-in defaults): less support than the
      default needs mode_reason
    - .project-knowledge/index.yaml and its entries, same rules as shared knowledge

Exit code: 0 clean, 1 errors (or warnings with --strict), 2 could not run.
Requires PyYAML (pip install pyyaml). No other dependencies.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    print("emw_check: PyYAML is required. Install it with: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

LEVELS = ["M0", "M1", "M2", "M3", "M4"]
ASSISTANCE = ["A0", "A1", "A2", "A3", "A4"]
ONBOARDING_STATUS = ["not-started", "in-progress", "complete", "needs-refresh"]
FRONTMATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*(\n|\Z)", re.S)


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, where: str, msg: str) -> None:
        self.errors.append(f"{where}: {msg}")

    def warn(self, where: str, msg: str) -> None:
        self.warnings.append(f"{where}: {msg}")


# --- minimal JSON Schema subset (the keywords EMW schemas use) -------------

def _is_date(value: object) -> bool:
    if isinstance(value, _dt.date):
        return True
    if not isinstance(value, str):
        return False
    try:
        _dt.date.fromisoformat(value)
        return True
    except ValueError:
        return False


def validate(value: object, schema: dict, path: str = "") -> list[str]:
    """Return a list of problems. Supports type, enum, const, required,
    properties, additionalProperties, items, minLength, pattern, format=date."""
    where = path or "(root)"
    problems: list[str] = []
    if "const" in schema and value != schema["const"]:
        return [f"{where}: must be {schema['const']!r}"]
    if "enum" in schema and value not in schema["enum"]:
        return [f"{where}: {value!r} is not one of {schema['enum']}"]
    expected = schema.get("type")
    if schema.get("format") == "date":
        if not _is_date(value):
            return [f"{where}: {value!r} is not a YYYY-MM-DD date"]
        return problems
    if expected == "object":
        if not isinstance(value, dict):
            return [f"{where}: expected an object"]
        for key in schema.get("required", []):
            if key not in value:
                problems.append(f"{where}: missing required field '{key}'")
        props = schema.get("properties", {})
        for key, sub in value.items():
            if key in props:
                problems += validate(sub, props[key], f"{path}.{key}" if path else key)
            elif schema.get("additionalProperties") is False:
                problems.append(f"{where}: unknown field '{key}'")
    elif expected == "array":
        if not isinstance(value, list):
            return [f"{where}: expected a list"]
        for i, item in enumerate(value):
            problems += validate(item, schema.get("items", {}), f"{path}[{i}]")
    elif expected == "integer":
        if not isinstance(value, int) or isinstance(value, bool):
            return [f"{where}: expected a whole number"]
        if "minimum" in schema and value < schema["minimum"]:
            problems.append(f"{where}: {value} is below {schema['minimum']}")
        if "maximum" in schema and value > schema["maximum"]:
            problems.append(f"{where}: {value} is above {schema['maximum']}")
    elif expected == "boolean":
        if not isinstance(value, bool):
            return [f"{where}: expected true or false"]
    elif expected == "string":
        if not isinstance(value, str):
            return [f"{where}: expected text"]
        if len(value) < schema.get("minLength", 0):
            problems.append(f"{where}: shorter than {schema['minLength']} characters")
        if "pattern" in schema and not re.search(schema["pattern"], value):
            problems.append(f"{where}: {value!r} does not match {schema['pattern']}")
    return problems


# --- helpers ----------------------------------------------------------------

def load_yaml(path: Path, rep: Report, root: Path):
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        rep.error(rel(path, root), f"invalid YAML: {exc}")
    except OSError as exc:
        rep.error(rel(path, root), f"cannot read: {exc}")
    return None


def load_frontmatter(path: Path, rep: Report, root: Path):
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER.match(text)
    if not match:
        rep.error(rel(path, root), "no YAML frontmatter (--- ... ---) at the top")
        return None
    try:
        data = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        rep.error(rel(path, root), f"invalid frontmatter YAML: {exc}")
        return None
    if not isinstance(data, dict):
        rep.error(rel(path, root), "frontmatter is not a mapping")
        return None
    return data


def rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def project_schema(schema: dict) -> dict:
    """Project knowledge may use PKB- ids (see project-knowledge-index template)."""
    clone = json.loads(json.dumps(schema))
    id_schema = clone["properties"]["id"]
    if "items" in clone["properties"].get("entries", {}):
        id_schema = clone["properties"]["entries"]["items"]["properties"]["id"]
    id_schema["pattern"] = "^P?KB-[A-Z0-9-]+$"
    return clone


# --- knowledge base check (shared or project) --------------------------------

def check_knowledge(kb_dir: Path, entry_schema: dict, index_schema: dict,
                    rep: Report, root: Path, label: str) -> int:
    index_path = kb_dir / "index.yaml"
    if not index_path.exists():
        rep.error(rel(kb_dir, root), "index.yaml is missing")
        return 0
    index = load_yaml(index_path, rep, root)
    if index is None:
        return 0
    for p in validate(index, index_schema):
        rep.error(rel(index_path, root), p)
    entries = (index.get("entries") or []) if isinstance(index, dict) else []

    seen_ids: dict[str, str] = {}
    indexed_files: set[Path] = set()
    for i, rec in enumerate(entries):
        if not isinstance(rec, dict):
            continue
        where = f"{rel(index_path, root)} entries[{i}]"
        rid = rec.get("id")
        if rid in seen_ids:
            rep.error(where, f"duplicate id {rid} (also used by {seen_ids[rid]})")
        elif rid:
            seen_ids[rid] = rec.get("path", "?")
        if not rec.get("path"):
            continue
        entry_path = (kb_dir / rec["path"]).resolve()
        indexed_files.add(entry_path)
        if not entry_path.exists():
            rep.error(where, f"path '{rec['path']}' does not exist")
            continue
        meta = load_frontmatter(entry_path, rep, root)
        if meta is None:
            continue
        for key in ("id", "title", "status", "confidence", "category"):
            if key in rec and key in meta and rec[key] != meta[key]:
                rep.error(where, f"index {key}={rec[key]!r} but entry says {meta[key]!r}")

    count = 0
    file_ids: dict[str, str] = {}
    for md in sorted(kb_dir.rglob("*.md")):
        if md.name.lower() == "readme.md":
            continue
        count += 1
        where = rel(md, root)
        if md.resolve() not in indexed_files:
            rep.error(where, "entry is not listed in index.yaml")
        meta = load_frontmatter(md, rep, root)
        if meta is None:
            continue
        mid = meta.get("id")
        if mid in file_ids:
            rep.error(where, f"id {mid} is also used by {file_ids[mid]}")
        elif mid:
            file_ids[mid] = where
        for p in validate(meta, entry_schema):
            rep.error(where, p)
        check_entry_rules(meta, where, rep, label)
    return count


def check_entry_rules(meta: dict, where: str, rep: Report, label: str) -> None:
    status = meta.get("status")
    evidence = meta.get("evidence") or []
    if status == "verified":
        if not evidence:
            rep.error(where, "status is verified but evidence is empty")
        elif all(isinstance(e, dict) and e.get("type") == "reasoned-guidance" for e in evidence):
            rep.error(where, "verified entries need evidence stronger than reasoned-guidance")
    if status == "superseded" and not meta.get("superseded_by"):
        rep.error(where, "status is superseded but superseded_by is empty")
    if not meta.get("limitations"):
        rep.warn(where, "no limitations listed; every entry has some")
    if label == "shared" and meta.get("scope") == "project-local":
        rep.error(where, "project-local entry inside the shared knowledge base")
    if label == "shared" and meta.get("source_project"):
        rep.warn(where, "shared entry names a source_project; confirm it is sanitised")
    for e in evidence:
        if isinstance(e, dict) and e.get("type") == "authoritative-source" and not e.get("uri"):
            rep.warn(where, "authoritative-source evidence without a uri")
    created, reviewed = meta.get("created_at"), meta.get("last_reviewed")
    if _is_date(created) and _is_date(reviewed) and str(reviewed) < str(created):
        rep.error(where, "last_reviewed is earlier than created_at")


# --- project records ----------------------------------------------------------

def check_project(root: Path, entry_schema: dict, index_schema: dict, rep: Report) -> bool:
    proj = root / ".emw-project"
    pkb = root / ".project-knowledge"
    if not proj.exists() and not pkb.exists():
        return False

    status_path = proj / "onboarding-status.yaml"
    if not status_path.exists():
        rep.warn(rel(proj, root), "onboarding-status.yaml missing; run the onboarding prompt (01)")
    else:
        data = load_yaml(status_path, rep, root) or {}
        where = rel(status_path, root)
        status = data.get("status")
        if status not in ONBOARDING_STATUS:
            rep.error(where, f"status {status!r} is not one of {ONBOARDING_STATUS}")
        if status == "complete":
            if not data.get("last_reviewed"):
                rep.error(where, "status is complete but last_reviewed is empty")
            for key in ("project_profile", "delivery_ledger", "skill_ledger"):
                target = data.get(key)
                if target and not (root / target).exists():
                    rep.error(where, f"{key} points to missing file {target}")

    ledger_path = proj / "skill-ledger.yaml"
    skills: dict[str, str] | None = None
    if ledger_path.exists():
        skills = check_skill_ledger(ledger_path, rep, root)

    policy = load_policy(proj / "mode-policy.yaml", rep, root)
    log_path = proj / "task-log.yaml"
    if log_path.exists():
        check_task_log(log_path, skills, policy, rep, root)

    if pkb.exists():
        check_knowledge(pkb, project_schema(entry_schema), project_schema(index_schema),
                        rep, root, "project")
    return True


def check_skill_ledger(path: Path, rep: Report, root: Path) -> dict[str, dict] | None:
    """Validate the ledger; return {skill id: {"level": .., "last_check": date or None}}.

    last_check is the latest evidence date produced with assistance A0-A2,
    i.e. the last time the developer showed the skill without solution-level AI help."""
    data = load_yaml(path, rep, root)
    if not isinstance(data, dict):
        return None
    where = rel(path, root)
    seen: set[str] = set()
    levels: dict[str, dict] = {}
    for i, skill in enumerate(data.get("skills") or []):
        if not isinstance(skill, dict):
            rep.error(where, f"skills[{i}] is not a mapping")
            continue
        sid = skill.get("id") or f"skills[{i}]"
        at = f"{where} {sid}"
        if sid in seen:
            rep.error(at, "duplicate skill id")
        seen.add(sid)
        for key in ("current_level", "target_level"):
            if skill.get(key) not in LEVELS:
                rep.error(at, f"{key} {skill.get(key)!r} is not one of {LEVELS}")
        if skill.get("scope") not in ("S1", "S2", "S3"):
            rep.error(at, f"scope {skill.get('scope')!r} is not S1, S2 or S3")
        if skill.get("confidence") not in ("low", "medium", "high"):
            rep.error(at, f"confidence {skill.get('confidence')!r} is not low, medium or high")
        level = skill.get("current_level")
        evidence = skill.get("evidence") or []
        if not isinstance(evidence, list):
            rep.error(at, "evidence must be a list")
            evidence = []
        checks = [str(e["date"]) for e in evidence if isinstance(e, dict)
                  and e.get("assistance") in ("A0", "A1", "A2") and _is_date(e.get("date"))]
        levels[sid] = {"level": level, "last_check": max(checks) if checks else None}
        if level in LEVELS and level != "M0" and not evidence:
            rep.error(at, f"current_level {level} has no evidence; use M0 until evidence exists")
        if level in ("M3", "M4"):
            independent = [e for e in evidence if isinstance(e, dict)
                           and e.get("assistance") in ("A0", "A1", "A2")]
            if not independent:
                rep.error(at, f"{level} needs at least one evidence item with assistance A0-A2 "
                              "(A3/A4 work cannot show independent application)")
            elif not any(e.get("verified_by") == "human" for e in independent):
                rep.error(at, f"{level} needs an A0-A2 evidence item with verified_by: human "
                              "(a lead or peer saw it; the agent cannot certify its own assessment)")
        for j, e in enumerate(evidence):
            if not isinstance(e, dict):
                continue
            if e.get("assistance") not in (None, *ASSISTANCE):
                rep.error(at, f"evidence[{j}] assistance {e.get('assistance')!r} is not A0-A4")
            if e.get("verified_by") not in (None, "human", "self"):
                rep.error(at, f"evidence[{j}] verified_by {e.get('verified_by')!r} is not human or self")
            if "date" in e and not _is_date(e.get("date")):
                rep.error(at, f"evidence[{j}] date {e.get('date')!r} is not YYYY-MM-DD")
        if level in LEVELS and skill.get("target_level") in LEVELS:
            if LEVELS.index(level) > LEVELS.index(skill["target_level"]):
                rep.warn(at, "current level is above target; raise the target or check the evidence")
    return levels


# --- mode policy and task log ---------------------------------------------------

DEFAULT_POLICY = {
    "default_mode_by_level": {"M0": 1, "M1": 1, "M2": 2, "M3": "any", "M4": "any"},
    "mode4_min_level": "M3",
    "assessment_every": 4,
}


def load_policy(path: Path, rep: Report, root: Path) -> dict:
    """Return the team mode policy, or the built-in defaults when absent or invalid."""
    if not path.exists():
        return {**DEFAULT_POLICY, "_builtin": True}
    data = load_yaml(path, rep, root)
    where = rel(path, root)
    if not isinstance(data, dict):
        rep.error(where, "mode policy is not a mapping; using built-in defaults")
        return {**DEFAULT_POLICY, "_builtin": True}
    policy = {**DEFAULT_POLICY, **data}
    table = policy.get("default_mode_by_level")
    if not isinstance(table, dict):
        rep.error(where, "default_mode_by_level must map M0-M4 to 1-4 or 'any'")
        policy["default_mode_by_level"] = DEFAULT_POLICY["default_mode_by_level"]
    else:
        for lvl in LEVELS:
            if table.get(lvl) not in (1, 2, 3, 4, "any"):
                rep.error(where, f"default_mode_by_level.{lvl} is {table.get(lvl)!r}; use 1-4 or 'any'")
    if policy.get("mode4_min_level") not in LEVELS:
        rep.error(where, f"mode4_min_level {policy.get('mode4_min_level')!r} is not one of {LEVELS}")
        policy["mode4_min_level"] = "M3"
    every = policy.get("assessment_every")
    if not isinstance(every, int) or isinstance(every, bool) or every < 1:
        rep.error(where, f"assessment_every {every!r} must be a whole number of tasks, 1 or more")
        policy["assessment_every"] = 4
    return policy


def check_task_log(path: Path, skills: dict[str, dict] | None, policy: dict,
                   rep: Report, root: Path) -> None:
    data = load_yaml(path, rep, root)
    where = rel(path, root)
    if data is None:
        return  # load_yaml already reported the problem
    if not isinstance(data, dict) or not isinstance(data.get("tasks", []), list):
        rep.error(where, "expected a mapping with a 'tasks' list")
        return
    tasks = data.get("tasks") or []
    if tasks and skills is None:
        rep.warn(where, "no skill-ledger.yaml; skill ids and mode policy cannot be checked")
    if tasks and policy.get("_builtin"):
        rep.warn(where, "no .emw-project/mode-policy.yaml; using built-in mode defaults")
    table = policy["default_mode_by_level"]
    min4 = LEVELS.index(policy["mode4_min_level"])
    seen: set[str] = set()

    for i, task in enumerate(tasks):
        if not isinstance(task, dict):
            rep.error(where, f"tasks[{i}] is not a mapping")
            continue
        tid = task.get("id") or f"tasks[{i}]"
        at = f"{where} {tid}"
        if not task.get("id"):
            rep.error(at, "missing id")
        elif tid in seen:
            rep.error(at, "duplicate task id")
        seen.add(tid)
        if not _is_date(task.get("date")):
            rep.error(at, f"date {task.get('date')!r} is not YYYY-MM-DD")
        if not task.get("summary"):
            rep.error(at, "missing summary")
        mode = task.get("mode")
        if mode not in (1, 2, 3, 4):
            rep.error(at, f"mode {mode!r} is not 1, 2, 3 or 4")
            mode = None
        assistance = task.get("assistance")
        if assistance not in ASSISTANCE:
            rep.error(at, f"assistance {assistance!r} is not one of {ASSISTANCE}")
        if mode == 1 and assistance == "A4":
            rep.warn(at, "Mode 1 (human implements) recorded as A4 (AI-authored); check which is true")
        task_skills = task.get("skills") or []
        if not isinstance(task_skills, list):
            rep.error(at, "skills must be a list of skill ids")
            continue
        if not task_skills:
            rep.warn(at, "no skills listed; the mode policy cannot be applied")
        if skills is None:
            continue

        known = []
        for sid in task_skills:
            if sid not in skills:
                rep.error(at, f"skill '{sid}' is not in skill-ledger.yaml")
            elif skills[sid]["level"] in LEVELS:
                known.append((sid, skills[sid]["level"]))
        if not known or mode is None:
            continue
        weakest_id, weakest = min(known, key=lambda kv: LEVELS.index(kv[1]))
        reason = str(task.get("mode_reason") or "").strip()
        default = table.get(weakest, "any")
        if default != "any" and mode > default and not reason:
            rep.error(at, f"mode {mode} gives less support than the policy default {default} for "
                          f"{weakest_id} ({weakest}); add mode_reason or use mode {default}")
        elif mode == 4 and LEVELS.index(weakest) < min4 and not reason:
            rep.error(at, f"Mode 4 on {weakest_id} ({weakest}) is below mode4_min_level "
                          f"{policy['mode4_min_level']}; add mode_reason")

    if skills:
        check_assessment_cadence(tasks, skills, policy["assessment_every"], rep, where)


def check_assessment_cadence(tasks: list, skills: dict[str, dict], every: int,
                             rep: Report, where: str) -> None:
    """Warn when a skill has been used in `every` or more logged tasks since its last
    no-AI check (latest A0-A2 evidence). Skills at M4 are exempt."""
    for sid, info in skills.items():
        if info["level"] == "M4":
            continue
        since = info["last_check"]
        count = sum(1 for t in tasks if isinstance(t, dict)
                    and isinstance(t.get("skills"), list) and sid in t["skills"]
                    and _is_date(t.get("date")) and (since is None or str(t["date"]) > since))
        if count >= every:
            last = f"since {since}" if since else "with no check without AI yet"
            rep.warn(f"{where} {sid}", f"used in {count} tasks {last}; run a short check without AI "
                                       "(see .emw/assessments/) and record it in skill-ledger.yaml")

# --- learning tracks ---------------------------------------------------------

def check_tracks(root: Path, rep: Report) -> int:
    """Validate .emw/tracks/*.yaml. Returns the number of track files checked."""
    tracks_dir = root / ".emw" / "tracks"
    if not tracks_dir.is_dir():
        return 0
    try:
        schema = json.loads((tracks_dir / "track.schema.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        rep.error(rel(tracks_dir, root), f"cannot load track.schema.json: {exc}")
        return 0

    tracks: dict[str, dict] = {}
    files: dict[str, Path] = {}
    for path in sorted(tracks_dir.glob("*.yaml")):
        data = load_yaml(path, rep, root)
        where = rel(path, root)
        if not isinstance(data, dict):
            if data is not None:
                rep.error(where, "track file is not a mapping")
            continue
        for problem in validate(data, schema):
            rep.error(where, problem)
        tid = data.get("id")
        if tid != path.stem:
            rep.error(where, f"id {tid!r} must match the file name '{path.stem}'")
        if isinstance(tid, str):
            if tid in tracks:
                rep.error(where, f"duplicate track id {tid}")
            tracks[tid] = data
            files[tid] = path

    for tid, data in tracks.items():
        where = rel(files[tid], root)
        own = {s.get("id"): s for s in data.get("skills") or [] if isinstance(s, dict)}
        if len(own) != len([s for s in data.get("skills") or [] if isinstance(s, dict)]):
            rep.error(where, "duplicate skill id in skills")
        known = set(own)
        parent = data.get("extends")
        if parent:
            if parent == tid:
                rep.error(where, "a track cannot extend itself")
            elif parent not in tracks:
                rep.error(where, f"extends '{parent}', but .emw/tracks/{parent}.yaml does not exist")
            else:
                known |= {s.get("id") for s in tracks[parent].get("skills") or [] if isinstance(s, dict)}

        stages = [s for s in data.get("stages") or [] if isinstance(s, dict)]
        numbers = [s.get("number") for s in stages]
        if numbers != sorted(numbers) or len(set(numbers)) != len(numbers):
            rep.error(where, f"stage numbers {numbers} must be unique and in ascending order")
        last_target: dict[str, str] = {}
        used: set[str] = set()
        for stage in stages:
            at = f"{where} stage {stage.get('number')}"
            seen_here: set[str] = set()
            for item in stage.get("skills") or []:
                if not isinstance(item, dict):
                    continue
                sid, target = item.get("id"), item.get("target")
                if sid in seen_here:
                    rep.error(at, f"skill '{sid}' is listed twice")
                seen_here.add(sid)
                if sid not in known:
                    rep.error(at, f"skill '{sid}' is not defined in this track or the one it extends")
                    continue
                used.add(sid)
                if target in LEVELS:
                    prev = last_target.get(sid)
                    if prev and LEVELS.index(target) < LEVELS.index(prev):
                        rep.error(at, f"target for '{sid}' drops from {prev} to {target}")
                    last_target[sid] = target
            brief = (stage.get("project") or {}).get("brief")
            if isinstance(brief, str) and not (tracks_dir / brief).is_file():
                rep.error(at, f"project brief '{brief}' does not exist under .emw/tracks/")
            if not stage.get("skills"):
                rep.warn(at, "stage lists no skills, so its gate checks nothing")
        for sid in sorted(set(own) - used):
            # the shared core defines skills that language tracks use later
            if not any(t.get("extends") == tid for t in tracks.values()):
                rep.warn(where, f"skill '{sid}' is defined but no stage uses it")
    return len(tracks)


# --- main -------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate EMW knowledge and project records.")
    parser.add_argument("--root", default=".", help="repository root (default: current directory)")
    parser.add_argument("--strict", action="store_true", help="treat warnings as errors")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    kb = root / ".emw" / "knowledge"
    try:
        entry_schema = json.loads((kb / "knowledge-entry.schema.json").read_text(encoding="utf-8"))
        index_schema = json.loads((kb / "knowledge-index.schema.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"emw_check: cannot load schemas from {kb}: {exc}", file=sys.stderr)
        return 2

    rep = Report()
    shared = check_knowledge(kb, entry_schema, index_schema, rep, root, "shared")
    has_project = check_project(root, entry_schema, index_schema, rep)
    track_count = check_tracks(root, rep)

    for w in rep.warnings:
        print(f"WARN  {w}")
    for e in rep.errors:
        print(f"ERROR {e}")
    scope = "shared knowledge + project records" if has_project else "shared knowledge"
    if track_count:
        scope += f" + {track_count} tracks"
    print(f"emw_check: {scope}; {shared} shared entries; "
          f"{len(rep.errors)} errors, {len(rep.warnings)} warnings")
    failed = rep.errors or (args.strict and rep.warnings)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
