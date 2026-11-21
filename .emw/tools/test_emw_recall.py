"""Tests for emw_recall. Run: python -m unittest discover -s .emw/tools -p "test_*.py" """
from __future__ import annotations

import contextlib
import datetime as dt
import io
import shutil
import tempfile
import textwrap
import unittest
from pathlib import Path

import yaml

import emw_check
import emw_recall

FRAMEWORK = Path(__file__).resolve().parents[2]

LEDGER = """\
version: 1
skills:
  - id: "php.pdo"
    name: "PDO"
    scope: "S1"
    target_level: "M3"
    current_level: "M2"
    confidence: "medium"
    evidence:
      - {date: "2026-11-01", type: implement, assistance: A1, verified_by: self, task: "built it"}
  - id: "php.untouched"
    name: "Not started"
    scope: "S1"
    target_level: "M3"
    current_level: "M0"
    confidence: "low"
    evidence: []
"""


class EmwRecallTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        shutil.copytree(FRAMEWORK / ".emw" / "knowledge", self.root / ".emw" / "knowledge")
        (self.root / ".emw-project").mkdir()
        self.write("skill-ledger.yaml", LEDGER)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def write(self, name: str, text: str) -> None:
        (self.root / ".emw-project" / name).write_text(textwrap.dedent(text), encoding="utf-8")

    def run_recall(self, *args: str) -> tuple[int, str]:
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = emw_recall.main(["--root", str(self.root), *args])
        return code, out.getvalue() + err.getvalue()

    def ledger(self) -> dict:
        return yaml.safe_load((self.root / ".emw-project" / "skill-ledger.yaml").read_text(encoding="utf-8"))

    def test_nothing_due_before_the_first_interval(self):
        code, out = self.run_recall("due", "--date", "2026-11-02")
        self.assertEqual(code, 0, out)
        self.assertIn("No recall check is due", out)

    def test_due_then_recorded_then_clear(self):
        code, out = self.run_recall("due", "--date", "2026-11-04")
        self.assertEqual(code, 1)
        self.assertIn("2-day", out)
        self.assertIn("php.pdo", out)
        # a skill with no evidence is never scheduled
        self.assertNotIn("php.untouched", out)

        code, out = self.run_recall("done", "php.pdo", "--task", "rebuilt it", "--date", "2026-11-04")
        self.assertEqual(code, 0, out)
        self.assertIn("7-day", out)  # tells the learner what comes next
        item = self.ledger()["skills"][0]["evidence"][-1]
        self.assertEqual(item, {"date": "2026-11-04", "type": "recall", "assistance": "A0",
                                "verified_by": "self", "task": "rebuilt it"})

        code, out = self.run_recall("due", "--date", "2026-11-04")
        self.assertEqual(code, 0, out)
        # the ledger still passes the checker after the tool rewrote it
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(emw_check.main(["--root", str(self.root)]), 0)

    def test_a_late_check_does_not_satisfy_an_earlier_slot(self):
        self.run_recall("done", "php.pdo", "--task", "late", "--date", "2026-11-20")
        code, out = self.run_recall("plan", "--date", "2026-11-20")
        self.assertEqual(code, 0, out)
        self.assertIn("missed", out)   # the 2-day slot closed unfilled
        self.assertIn("done", out)     # the 7-day slot took the late check

    def test_an_a3_rebuild_does_not_count(self):
        ledger = self.ledger()
        ledger["skills"][0]["evidence"].append(
            {"date": "2026-11-04", "type": "rebuild", "assistance": "A3",
             "verified_by": "self", "task": "with the agent writing"})
        (self.root / ".emw-project" / "skill-ledger.yaml").write_text(
            yaml.safe_dump(ledger, sort_keys=False), encoding="utf-8")
        code, out = self.run_recall("due", "--date", "2026-11-04")
        self.assertEqual(code, 1, out)
        self.assertIn("2-day", out)

    def test_policy_can_change_or_switch_off_the_schedule(self):
        self.write("mode-policy.yaml", """\
            version: 1
            recall_days: [1]
            """)
        code, out = self.run_recall("due", "--date", "2026-11-02")
        self.assertEqual(code, 1, out)
        self.assertIn("1-day", out)

        self.write("mode-policy.yaml", """\
            version: 1
            recall_days: []
            """)
        code, out = self.run_recall("plan", "--date", "2026-12-31")
        self.assertEqual(code, 0, out)
        self.assertIn("no recall check is scheduled", out)

    def test_bad_recall_days_is_an_error_and_falls_back(self):
        self.write("mode-policy.yaml", """\
            version: 1
            recall_days: [7, 2]
            """)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = emw_check.main(["--root", str(self.root), "--date", "2026-11-04"])
        self.assertEqual(code, 1)
        self.assertIn("rising order", out.getvalue())

    def test_checker_reports_a_due_check_as_a_note_not_a_failure(self):
        shutil.copy(FRAMEWORK / ".emw" / "templates" / "onboarding-status.yaml",
                    self.root / ".emw-project" / "onboarding-status.yaml")
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = emw_check.main(["--root", str(self.root), "--strict", "--date", "2026-11-04"])
        text = out.getvalue()
        self.assertIn("NOTE", text)
        self.assertIn("2-day recall check is due", text)
        self.assertEqual(code, 0, text)  # notes never fail the build, even with --strict

    def test_missing_ledger_is_a_clear_message(self):
        (self.root / ".emw-project" / "skill-ledger.yaml").unlink()
        code, out = self.run_recall("due")
        self.assertEqual(code, 2)
        self.assertIn("no skill ledger", out)

    def test_unknown_skill_lists_the_known_ones(self):
        code, out = self.run_recall("done", "php.nope", "--task", "x")
        self.assertEqual(code, 2)
        self.assertIn("php.pdo", out)

    def test_schedule_slots_are_exact(self):
        skill = self.ledger()["skills"][0]
        slots = emw_check.recall_schedule(skill, dt.date(2026, 11, 4), [2, 7, 30])
        self.assertEqual([s["days"] for s in slots], [2, 7, 30])
        self.assertEqual(slots[0]["due"], dt.date(2026, 11, 3))
        self.assertEqual([s["state"] for s in slots], ["due", "upcoming", "upcoming"])


if __name__ == "__main__":
    unittest.main()
