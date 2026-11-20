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
  Project records (only when .emw-project/ or .project-knowledge/ exist)
    - onboarding-status.yaml status and referenced files
    - skill-ledger.yaml levels, and M3/M4 claims backed by evidence
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
    if ledger_path.exists():
        check_skill_ledger(ledger_path, rep, root)

    if pkb.exists():
        check_knowledge(pkb, project_schema(entry_schema), project_schema(index_schema),
                        rep, root, "project")
    return True


def check_skill_ledger(path: Path, rep: Report, root: Path) -> None:
    data = load_yaml(path, rep, root)
    if not isinstance(data, dict):
        return
    where = rel(path, root)
    seen: set[str] = set()
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
        if level in LEVELS and level != "M0" and not evidence:
            rep.error(at, f"current_level {level} has no evidence; use M0 until evidence exists")
        if level in ("M3", "M4"):
            independent = [e for e in evidence if isinstance(e, dict)
                           and e.get("assistance") in ("A0", "A1", "A2")]
            if not independent:
                rep.error(at, f"{level} needs at least one evidence item with assistance A0-A2 "
                              "(A3/A4 work cannot show independent application)")
        for j, e in enumerate(evidence):
            if isinstance(e, dict) and e.get("assistance") not in (None, *ASSISTANCE):
                rep.error(at, f"evidence[{j}] assistance {e.get('assistance')!r} is not A0-A4")
        if level in LEVELS and skill.get("target_level") in LEVELS:
            if LEVELS.index(level) > LEVELS.index(skill["target_level"]):
                rep.warn(at, "current level is above target; raise the target or check the evidence")


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

    for w in rep.warnings:
        print(f"WARN  {w}")
    for e in rep.errors:
        print(f"ERROR {e}")
    scope = "shared knowledge + project records" if has_project else "shared knowledge"
    print(f"emw_check: {scope}; {shared} shared entries; "
          f"{len(rep.errors)} errors, {len(rep.warnings)} warnings")
    failed = rep.errors or (args.strict and rep.warnings)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
