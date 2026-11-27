"""End-to-end test of the path a new learner actually walks.

Run: python -m unittest discover -s .emw/tools -p "test_*.py"

The unit tests around these tools all passed while the recall scheduler was inert for
every skill a track creates, because each of them started from a skill at M2 and a
learner starts at M0. This file exists to catch that class of defect: it installs the
framework into an empty directory and walks one learner from `start` to passing the
Stage 1 gate, asserting the behaviour at each step rather than any one function.

Dates are fixed so the seven-day rebuild rule and the recall schedule are deterministic.
Every evidence item it writes is a fixture; none of it describes work anyone did.
"""
from __future__ import annotations

import contextlib
import io
import shutil
import tempfile
import unittest
from pathlib import Path

import yaml

import emw_check
import emw_recall
import emw_track

FRAMEWORK = Path(__file__).resolve().parents[2]

STAGE_BEGAN = "2026-11-01"
FIRST_WORK = "2026-11-02"
REBUILD_DAY = "2026-11-10"   # more than 7 days after the stage began
GATE_DAY = "2026-11-20"


class FreshLearnerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        for part in ("knowledge", "tracks", "templates"):
            shutil.copytree(FRAMEWORK / ".emw" / part, self.root / ".emw" / part)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    # --- helpers ----------------------------------------------------------------

    def track(self, *args: str) -> tuple[int, str]:
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
            code = emw_track.main(["--root", str(self.root), *args])
        return code, out.getvalue()

    def recall(self, *args: str) -> tuple[int, str]:
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
            code = emw_recall.main(["--root", str(self.root), *args])
        return code, out.getvalue()

    def check(self, *args: str) -> tuple[int, str]:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = emw_check.main(["--root", str(self.root), *args])
        return code, out.getvalue()

    def ledger(self) -> dict:
        return yaml.safe_load(
            (self.root / ".emw-project/skill-ledger.yaml").read_text(encoding="utf-8"))

    def save_ledger(self, data: dict) -> None:
        (self.root / ".emw-project/skill-ledger.yaml").write_text(
            yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")

    def evidence(self, skill_id: str, item: dict) -> None:
        data = self.ledger()
        skill = next(s for s in data["skills"] if s["id"] == skill_id)
        skill.setdefault("evidence", []).append(item)
        self.save_ledger(data)

    def onboard(self) -> None:
        """Write the records prompt 01 requires, as /emw-onboard would."""
        proj = self.root / ".emw-project"
        shutil.copy(FRAMEWORK / ".emw/templates/onboarding-status.yaml",
                    proj / "onboarding-status.yaml")
        (proj / "project-profile.md").write_text("# Project Profile\n", encoding="utf-8")
        (proj / "delivery-ledger.md").write_text("# Engineering Delivery Ledger\n", encoding="utf-8")
        pkb = self.root / ".project-knowledge"
        pkb.mkdir()
        (pkb / "README.md").write_text("# Project Knowledge Base\n", encoding="utf-8")
        (pkb / "index.yaml").write_text(
            'schema_version: 1\nproject: "demo"\nupdated_at: "2026-11-01"\nentries: []\n',
            encoding="utf-8")
        status = proj / "onboarding-status.yaml"
        status.write_text(status.read_text(encoding="utf-8")
                          .replace('status: "not-started"', 'status: "complete"')
                          .replace('last_reviewed: ""', f'last_reviewed: "{STAGE_BEGAN}"'),
                          encoding="utf-8")

    # --- the walk ---------------------------------------------------------------

    def test_a_learner_can_reach_stage_two(self):
        # 1. Starting a track is not onboarding, and says so.
        code, out = self.track("start", "php", "--date", STAGE_BEGAN)
        self.assertEqual(code, 0, out)
        self.assertIn("not onboarded", out)
        self.assertIn("stage 1", out)
        proj = self.root / ".emw-project"
        self.assertFalse((proj / "onboarding-status.yaml").exists())
        for name in ("track.yaml", "skill-ledger.yaml", "task-log.yaml", "mode-policy.yaml"):
            self.assertTrue((proj / name).exists(), name)

        # The ledger keeps the template's shape, and names the track.
        data = self.ledger()
        self.assertIn("levels", data)
        self.assertIn("assistance", data)
        self.assertEqual(data["project"], "PHP with Laravel learning track")
        # Stage 1 has 8 skills: core.terminal, core.git, php.syntax-types,
        # php.arrays-functions, php.files-errors, php.composer-autoload,
        # php.testing-pest, core.testing
        self.assertTrue(all(s["current_level"] == "M0" for s in data["skills"]))

        # 2. The checker names what onboarding still owes, without failing the run.
        code, out = self.check()
        self.assertEqual(code, 0, out)
        for record in ("onboarding-status.yaml", "project-profile.md", "delivery-ledger.md",
                       ".project-knowledge/README.md", ".project-knowledge/index.yaml"):
            self.assertIn(record, out)
        self.assertEqual(self.check("--strict")[0], 1)

        # The gate explains a ticked check row that still reports warnings.
        code, out = self.track("status")
        self.assertEqual(code, 0, out)
        self.assertIn("[x] check", out)
        self.assertIn("warnings do not block the gate", out)

        # 3. A skill at M0 owes recall checks once it has dated evidence.
        #    This is the regression that mattered: every skill a track creates is M0.
        self.assertIn("No skill has dated evidence yet", self.recall("plan")[1])
        self.evidence("php.syntax-types", {
            "date": FIRST_WORK, "type": "implement", "assistance": "A1",
            "verified_by": "self", "task": "fixture: first PHP exercises"})
        code, out = self.recall("due", "--date", "2026-11-05")
        self.assertEqual(code, 1, out)
        self.assertIn("php.syntax-types", out)
        self.assertIn("2-day", out)

        # 4. A recall check recorded by the tool satisfies the gate's rebuild item,
        #    although the tool writes type: recall and the gate speaks of rebuild.
        code, out = self.recall("done", "php.syntax-types", "--task", "fixture: rebuilt from memory",
                                "--date", REBUILD_DAY)
        self.assertEqual(code, 0, out)
        php_st = next(s for s in self.ledger()["skills"] if s["id"] == "php.syntax-types")
        recorded = php_st["evidence"][-1]
        self.assertEqual(recorded["type"], "recall")
        self.assertEqual(recorded["assistance"], "A0")

        # 5. Onboarding clears every warning.
        self.onboard()
        code, out = self.check("--strict")
        self.assertEqual(code, 0, out)

        # 6. Meet the rest of the gate, as a learner and their mentor would.
        data = self.ledger()
        targets = {"core.terminal": "M2", "core.git": "M3",
                   "php.syntax-types": "M3", "php.arrays-functions": "M3",
                   "php.files-errors": "M2", "php.composer-autoload": "M2",
                   "php.testing-pest": "M2", "core.testing": "M2"}
        for skill in data["skills"]:
            skill["current_level"] = targets[skill["id"]]
            skill.setdefault("evidence", []).append({
                "date": FIRST_WORK, "type": "implement", "assistance": "A1",
                "verified_by": "self", "task": "fixture: stage 1 work"})
        self.save_ledger(data)
        self.evidence("core.git", {
            "date": REBUILD_DAY, "type": "implement", "assistance": "A1",
            "verified_by": "human", "task": "fixture: a mentor reviewed the tool"})
        # M3 skills need human-verified evidence to pass emw_check
        self.evidence("php.syntax-types", {
            "date": REBUILD_DAY, "type": "implement", "assistance": "A1",
            "verified_by": "human", "task": "fixture: mentor reviewed types"})
        self.evidence("php.arrays-functions", {
            "date": REBUILD_DAY, "type": "implement", "assistance": "A1",
            "verified_by": "human", "task": "fixture: mentor reviewed arrays"})
        self.evidence("php.arrays-functions", {
            "date": REBUILD_DAY, "type": "transfer", "assistance": "A1",
            "verified_by": "self", "task": "fixture: the brief's stretch change"})
        code, out = self.track("ship", "--url", "https://example.test/hesabu")
        self.assertEqual(code, 0, out)

        code, out = self.track("status")
        for item in ("[x] shipped", "[x] levels", "[x] human", "[x] rebuild",
                     "[x] transfer", "[x] check"):
            self.assertIn(item, out)

        # 7. The gate opens, which is the one path no other test reaches.
        code, out = self.track("next", "--date", GATE_DAY)
        self.assertEqual(code, 0, out)
        self.assertIn("Now on stage 2", out)
        self.assertIn("php.oop", [s["id"] for s in self.ledger()["skills"]])
        self.assertIn("core.html-css", [s["id"] for s in self.ledger()["skills"]])
        self.assertEqual(self.check("--strict")[0], 0)

    def test_the_gate_refuses_and_says_what_is_missing(self):
        self.track("start", "php", "--date", STAGE_BEGAN)
        self.onboard()
        code, out = self.track("next", "--date", GATE_DAY)
        self.assertEqual(code, 1, out)
        for item in ("shipped", "levels", "human", "rebuild", "transfer"):
            self.assertIn(item, out)
        # Nothing moved.
        state = yaml.safe_load((self.root / ".emw-project/track.yaml").read_text(encoding="utf-8"))
        self.assertEqual(state["current_stage"], 1)

    def test_an_early_rebuild_does_not_open_the_gate(self):
        """The seven-day wait is the point of the rebuild item."""
        self.track("start", "php", "--date", STAGE_BEGAN)
        self.evidence("php.syntax-types", {
            "date": "2026-11-03", "type": "rebuild", "assistance": "A0",
            "verified_by": "self", "task": "fixture: rebuilt two days in"})
        code, out = self.track("status")
        self.assertIn("[ ] rebuild", out)


if __name__ == "__main__":
    unittest.main()
