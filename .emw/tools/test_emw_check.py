"""Regression tests for emw_check. Run: python -m unittest discover -s .emw/tools -p "test_*.py"

Each test copies the framework's schemas and seed knowledge into a temp repo,
adds project records, and checks the exact problems the checker reports.
"""
from __future__ import annotations

import contextlib
import io
import shutil
import tempfile
import textwrap
import unittest
from pathlib import Path

import emw_check

FRAMEWORK = Path(__file__).resolve().parents[2]


class Repo:
    def __init__(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        shutil.copytree(FRAMEWORK / ".emw" / "knowledge", self.root / ".emw" / "knowledge")

    def write(self, rel: str, text: str) -> None:
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(textwrap.dedent(text), encoding="utf-8")

    def template(self, name: str) -> None:
        dest = self.root / ".emw-project" / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(FRAMEWORK / ".emw" / "templates" / name, dest)

    def run(self, *extra: str) -> tuple[int, str]:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = emw_check.main(["--root", str(self.root), *extra])
        return code, out.getvalue()

    def close(self) -> None:
        self.tmp.cleanup()


LEDGER = """\
skills:
  - id: php.sessions
    name: PHP sessions
    scope: S1
    target_level: M3
    current_level: M1
    confidence: low
    evidence:
      - {date: "2026-11-01", type: explain, assistance: A1, verified_by: self}
  - id: php.pdo
    name: PDO
    scope: S1
    target_level: M3
    current_level: M3
    confidence: high
    evidence:
      - {date: "2026-11-02", type: implement, assistance: A0, verified_by: human}
"""


class EmwCheckTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = Repo()

    def tearDown(self) -> None:
        self.repo.close()

    def test_framework_repo_is_clean(self):
        code, out = emw_check.main(["--root", str(FRAMEWORK), "--strict"]), ""
        self.assertEqual(code, 0)

    def test_onboarding_templates_pass(self):
        for name in ("onboarding-status.yaml", "skill-ledger.yaml", "task-log.yaml", "mode-policy.yaml"):
            self.repo.template(name)
        code, out = self.repo.run("--strict")
        self.assertEqual(code, 0, out)

    def test_unindexed_entry_and_bad_category(self):
        src = self.repo.root / ".emw/knowledge/debugging-playbooks/bisect-regressions.md"
        text = src.read_text(encoding="utf-8").replace('category: "debugging"', 'category: "debug"', 1)
        self.repo.write(".emw/knowledge/debugging-playbooks/orphan.md",
                        text.replace("KB-DBG-0001", "KB-DBG-0099"))
        code, out = self.repo.run()
        self.assertEqual(code, 1)
        self.assertIn("orphan.md: entry is not listed in index.yaml", out)
        self.assertIn("'debug' is not one of", out)

    def test_verified_needs_strong_evidence(self):
        path = self.repo.root / ".emw/knowledge/agent-guidance/report-unrun-checks.md"
        path.write_text(path.read_text(encoding="utf-8").replace(
            'status: "proposed"', 'status: "verified"', 1), encoding="utf-8")
        _, out = self.repo.run()
        self.assertIn("verified entries need evidence stronger than reasoned-guidance", out)

    def test_m3_needs_human_verified_low_help_evidence(self):
        self.repo.write(".emw-project/skill-ledger.yaml", """\
            skills:
              - id: a
                name: A
                scope: S1
                target_level: M3
                current_level: M3
                confidence: high
                evidence: [{date: "2026-11-01", type: implement, assistance: A4, verified_by: human}]
              - id: b
                name: B
                scope: S1
                target_level: M3
                current_level: M3
                confidence: high
                evidence: [{date: "2026-11-01", type: implement, assistance: A1, verified_by: self}]
            """)
        _, out = self.repo.run()
        self.assertIn("a: M3 needs at least one evidence item with assistance A0-A2", out)
        self.assertIn("b: M3 needs an A0-A2 evidence item with verified_by: human", out)

    def test_mode_policy_requires_reason(self):
        self.repo.write(".emw-project/skill-ledger.yaml", LEDGER)
        self.repo.template("mode-policy.yaml")
        self.repo.write(".emw-project/task-log.yaml", """\
            tasks:
              - {id: T-1, date: "2026-11-10", summary: s, mode: 4, assistance: A4, skills: [php.sessions]}
              - {id: T-2, date: "2026-11-10", summary: s, mode: 4, assistance: A4, skills: [php.sessions], mode_reason: "outage"}
              - {id: T-3, date: "2026-11-10", summary: s, mode: 4, assistance: A4, skills: [php.pdo]}
              - {id: T-4, date: "2026-11-10", summary: s, mode: 1, assistance: A1, skills: [laravel]}
            """)
        code, out = self.repo.run()
        self.assertEqual(code, 1)
        self.assertIn("T-1: mode 4 gives less support than the policy default 1", out)
        self.assertNotIn("T-2:", out)
        self.assertNotIn("T-3:", out)
        self.assertIn("T-4: skill 'laravel' is not in skill-ledger.yaml", out)

    def test_assessment_cadence_warns(self):
        self.repo.write(".emw-project/skill-ledger.yaml", LEDGER)
        self.repo.template("mode-policy.yaml")
        tasks = "\n".join(
            f'  - {{id: T-{i}, date: "2026-11-1{i}", summary: s, mode: 1, assistance: A1, skills: [php.sessions]}}'
            for i in range(4))
        self.repo.write(".emw-project/task-log.yaml", "tasks:\n" + tasks + "\n")
        code, out = self.repo.run()
        self.assertEqual(code, 0, out)  # warning only
        self.assertIn("php.sessions: used in 4 tasks since 2026-11-01", out)
        code, _ = self.repo.run("--strict")
        self.assertEqual(code, 1)


if __name__ == "__main__":
    unittest.main()
