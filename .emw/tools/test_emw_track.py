"""Tests for emw_track. Run: python -m unittest discover -s .emw/tools -p "test_*.py" """
from __future__ import annotations

import contextlib
import io
import shutil
import tempfile
import unittest
from pathlib import Path

import yaml

import emw_check
import emw_track

FRAMEWORK = Path(__file__).resolve().parents[2]


class EmwTrackTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        for part in ("knowledge", "tracks", "templates"):
            shutil.copytree(FRAMEWORK / ".emw" / part, self.root / ".emw" / part)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_track(self, *args: str) -> tuple[int, str]:
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = emw_track.main(["--root", str(self.root), *args])
        return code, out.getvalue() + err.getvalue()

    def ledger(self) -> dict:
        return yaml.safe_load((self.root / ".emw-project/skill-ledger.yaml").read_text(encoding="utf-8"))

    def save_ledger(self, data: dict) -> None:
        (self.root / ".emw-project/skill-ledger.yaml").write_text(
            yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    def test_start_creates_valid_project(self):
        code, out = self.run_track("start", "php", "--date", "2026-11-01")
        self.assertEqual(code, 0, out)
        self.assertIn("stage 0: Ground floor", out)
        ids = [s["id"] for s in self.ledger()["skills"]]
        self.assertEqual(ids, ["core.terminal", "core.git", "core.html-css", "core.http", "core.sql"])
        check_out = io.StringIO()
        with contextlib.redirect_stdout(check_out):
            self.assertEqual(emw_check.main(["--root", str(self.root), "--strict"]), 0, check_out.getvalue())

    def test_every_shipped_track_starts_cleanly(self):
        for track in ("php", "dotnet", "go", "python"):
            with self.subTest(track=track):
                shutil.rmtree(self.root / ".emw-project", ignore_errors=True)
                code, out = self.run_track("start", track, "--date", "2026-11-01")
                self.assertEqual(code, 0, out)
                self.assertIn("stage 0: Ground floor", out)
                check_out = io.StringIO()
                with contextlib.redirect_stdout(check_out):
                    self.assertEqual(emw_check.main(["--root", str(self.root), "--strict"]), 0,
                                     check_out.getvalue())

    def test_unknown_track_and_double_start(self):
        code, out = self.run_track("start", "cobol")
        self.assertEqual(code, 2)
        self.assertIn("no track 'cobol'", out)
        self.run_track("start", "php")
        code, out = self.run_track("start", "php")
        self.assertEqual(code, 2)
        self.assertIn("already started", out)

    def test_gate_blocks_then_opens_stage_one(self):
        self.run_track("start", "php", "--date", "2026-11-01")
        code, out = self.run_track("next", "--date", "2026-11-20")
        self.assertEqual(code, 1)
        for item in ("shipped", "levels", "human", "rebuild", "transfer"):
            self.assertIn(item, out)

        # levels reached with self-verified evidence only: human, rebuild and transfer still missing
        ledger = self.ledger()
        targets = {"core.terminal": "M2", "core.git": "M2", "core.html-css": "M2",
                   "core.http": "M1", "core.sql": "M1"}
        for skill in ledger["skills"]:
            skill["current_level"] = targets[skill["id"]]
            skill["evidence"] = [{"date": "2026-11-05", "type": "implement", "assistance": "A1",
                                  "verified_by": "self", "task": "stage 0 work"}]
        self.save_ledger(ledger)
        self.run_track("ship", "--url", "https://example.test/me")
        code, out = self.run_track("next", "--date", "2026-11-20")
        self.assertEqual(code, 1)
        self.assertNotIn("levels", out)
        self.assertNotIn("shipped", out)
        self.assertIn("human", out)

        # a rebuild only two days in does not count; one after a week does
        ledger = self.ledger()
        git = next(s for s in ledger["skills"] if s["id"] == "core.git")
        git["evidence"] += [
            {"date": "2026-11-03", "type": "rebuild", "assistance": "A0", "verified_by": "self", "task": "too early"},
            {"date": "2026-11-10", "type": "transfer", "assistance": "A1", "verified_by": "human", "task": "stretch"},
        ]
        self.save_ledger(ledger)
        code, out = self.run_track("next", "--date", "2026-11-20")
        self.assertEqual(code, 1)
        self.assertIn("rebuild", out)
        self.assertNotIn("human", out)
        self.assertNotIn("transfer", out)

        ledger = self.ledger()
        git = next(s for s in ledger["skills"] if s["id"] == "core.git")
        git["evidence"].append({"date": "2026-11-12", "type": "rebuild", "assistance": "A0",
                                "verified_by": "self", "task": "new repo from memory"})
        self.save_ledger(ledger)
        code, out = self.run_track("next", "--date", "2026-11-20")
        self.assertEqual(code, 0, out)
        self.assertIn("Now on stage 1: Language foundations", out)
        self.assertIn("raised core.git target to M3", out)

        ledger = self.ledger()
        ids = [s["id"] for s in ledger["skills"]]
        self.assertIn("php.syntax-types", ids)
        self.assertEqual(len(ids), len(set(ids)))
        # evidence from stage 0 does not count toward the stage 1 gate
        code, out = self.run_track("status")
        self.assertIn("Stage 1: Language foundations", out)
        self.assertIn("[ ] human", out)


if __name__ == "__main__":
    unittest.main()
