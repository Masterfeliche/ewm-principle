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

    def onboard(self, status: str = "not-started") -> None:
        """Write the full record set prompt 01 requires."""
        for name in ("onboarding-status.yaml", "skill-ledger.yaml", "task-log.yaml", "mode-policy.yaml"):
            self.repo.template(name)
        self.repo.write(".emw-project/project-profile.md", "# Project Profile\n")
        self.repo.write(".emw-project/delivery-ledger.md", "# Engineering Delivery Ledger\n")
        self.repo.write(".project-knowledge/README.md", "# Project Knowledge Base\n")
        self.repo.write(".project-knowledge/index.yaml",
                        'schema_version: 1\nproject: "demo"\nupdated_at: "2026-11-21"\nentries: []\n')
        if status != "not-started":
            path = self.repo.root / ".emw-project/onboarding-status.yaml"
            path.write_text(path.read_text(encoding="utf-8")
                            .replace('status: "not-started"', f'status: "{status}"')
                            .replace('last_reviewed: ""', 'last_reviewed: "2026-11-21"'), encoding="utf-8")

    def test_onboarding_templates_pass(self):
        self.onboard()
        code, out = self.repo.run("--strict")
        self.assertEqual(code, 0, out)

    def test_complete_onboarding_must_really_have_project_knowledge(self):
        """onboarding-status.yaml points at .project-knowledge/, but that pointer was
        never checked, so a project could claim completion with the directory gone."""
        self.onboard(status="complete")
        code, out = self.repo.run()
        self.assertEqual(code, 0, out)
        shutil.rmtree(self.repo.root / ".project-knowledge")
        code, out = self.repo.run()
        self.assertEqual(code, 1, out)
        self.assertIn("project_knowledge", out)

    def test_an_incomplete_record_set_warns(self):
        self.repo.template("skill-ledger.yaml")
        code, out = self.repo.run()
        self.assertEqual(code, 0, out)
        for missing in ("project-profile.md", "delivery-ledger.md", "task-log.yaml",
                        ".project-knowledge/index.yaml"):
            self.assertIn(missing, out)
        code, out = self.repo.run("--strict")
        self.assertEqual(code, 1, out)

    def test_unindexed_entry_and_bad_category(self):
        src = self.repo.root / ".emw/knowledge/debugging-playbooks/bisect-regressions.md"
        text = src.read_text(encoding="utf-8").replace('category: "debugging"', 'category: "debug"', 1)
        self.repo.write(".emw/knowledge/debugging-playbooks/orphan.md",
                        text.replace("KB-DBG-0001", "KB-DBG-0099"))
        code, out = self.repo.run()
        self.assertEqual(code, 1)
        self.assertIn("orphan.md: entry is not listed in index.yaml", out)
        self.assertIn("'debug' is not one of", out)

    def test_pkb_ids_only_in_project_knowledge(self):
        src = self.repo.root / ".emw/knowledge/debugging-playbooks/bisect-regressions.md"
        text = src.read_text(encoding="utf-8")
        self.repo.write(".project-knowledge/debugging/bisect.md", text.replace("KB-DBG-0001", "PKB-0001"))
        self.repo.template("onboarding-status.yaml")
        self.repo.write(".project-knowledge/index.yaml", """            schema_version: 1
            project: "demo"
            updated_at: "2026-11-21"
            entries:
              - id: "PKB-0001"
                title: "Find the commit that introduced a regression with git bisect"
                path: "debugging/bisect.md"
                category: "debugging"
                status: "proposed"
                confidence: "high"
            """)
        code, out = self.repo.run()
        self.assertEqual(code, 0, out)
        index = self.repo.root / ".emw/knowledge/index.yaml"
        index.write_text(index.read_text(encoding="utf-8").replace("KB-DBG-0001", "PKB-DBG-0001"), encoding="utf-8")
        src.write_text(text.replace("KB-DBG-0001", "PKB-DBG-0001"), encoding="utf-8")
        code, out = self.repo.run()
        self.assertEqual(code, 1, out)
        self.assertIn("PKB-DBG-0001", out)

    def test_the_shipped_schemas_accept_a_project_entry(self):
        """The schema files carried ^KB- while the templates mandate PKB-, so the
        documented 'validate against this schema' step failed every project entry."""
        import json
        entry = json.loads((self.repo.root / ".emw/knowledge/knowledge-entry.schema.json")
                           .read_text(encoding="utf-8"))
        index = json.loads((self.repo.root / ".emw/knowledge/knowledge-index.schema.json")
                           .read_text(encoding="utf-8"))
        self.assertEqual([], emw_check.validate(
            "PKB-0001", entry["properties"]["id"], "id"))
        self.assertEqual([], emw_check.validate(
            "KB-SEC-0001", index["properties"]["entries"]["items"]["properties"]["id"], "id"))
        self.assertEqual([], emw_check.validate("demo", index["properties"]["project"], "project"))
        self.assertTrue(emw_check.validate("nope", entry["properties"]["id"], "id"))

    def test_id_prefix_is_enforced_by_where_the_entry_lives(self):
        self.assertIsNone(emw_check.id_prefix_problem("PKB-0001", "project"))
        self.assertIsNone(emw_check.id_prefix_problem("KB-SEC-0001", "shared"))
        self.assertIn("shared", emw_check.id_prefix_problem("PKB-0001", "shared"))
        self.assertIn("PKB-", emw_check.id_prefix_problem("KB-0001", "project"))

    def test_counts_read_as_english(self):
        self.repo.write(".project-knowledge/index.yaml", """            schema_version: 1
            project: "demo"
            entries:
              - id: "PKB-0001"
                title: "An entry whose file was never written"
                path: "learning/absent.md"
                category: "learning"
                status: "draft"
                confidence: "low"
            """)
        code, out = self.repo.run()
        self.assertEqual(code, 1, out)
        self.assertIn("1 error,", out)
        self.assertNotIn("1 errors", out)
        self.assertIn("shared entries", out)

    def test_a_dangling_markdown_link_warns(self):
        """A link that resolves in the framework repository can still dangle in every
        install, because only .emw/, AGENTS.md and one adapter are copied."""
        self.repo.write("CLAUDE.md", "See [the guide](docs/MISSING.md) and [upstream](https://example.test/x).\n")
        code, out = self.repo.run()
        self.assertEqual(code, 0, out)
        self.assertIn("CLAUDE.md:1", out)
        self.assertIn("docs/MISSING.md", out)
        self.assertNotIn("example.test", out)
        code, out = self.repo.run("--strict")
        self.assertEqual(code, 1, out)

    def test_links_that_resolve_are_quiet(self):
        self.repo.write("docs/REAL.md", "# Real\n")
        self.repo.write("CLAUDE.md", "See [the guide](docs/REAL.md) and [an anchor](#part).\n")
        code, out = self.repo.run("--strict")
        self.assertEqual(code, 0, out)

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

    def _copy_tracks(self):
        shutil.copytree(FRAMEWORK / ".emw" / "tracks", self.repo.root / ".emw" / "tracks")
        return self.repo.root / ".emw" / "tracks" / "php.yaml"

    def test_shipped_tracks_pass(self):
        self._copy_tracks()
        code, out = self.repo.run("--strict")
        self.assertEqual(code, 0, out)
        self.assertIn("5 tracks", out)

    def test_track_rules_catch_planted_errors(self):
        php = self._copy_tracks()
        text = php.read_text(encoding="utf-8")
        # unknown skill, a target that goes down, and a missing brief
        text = text.replace("- {id: php.syntax-types, target: M3}",
                            "- {id: php.syntax-types, target: M3}\n      - {id: php.nonexistent, target: M2}", 1)
        text = text.replace("- {id: php.oop, target: M3}",
                            "- {id: php.oop, target: M3}\n      - {id: php.syntax-types, target: M1}", 1)
        text = text.replace('brief: "briefs/php-stage-5.md"', 'brief: "briefs/missing.md"', 1)
        php.write_text(text, encoding="utf-8")
        code, out = self.repo.run()
        self.assertEqual(code, 1)
        self.assertIn("stage 1: skill 'php.nonexistent' is not defined", out)
        self.assertIn("stage 2: target for 'php.syntax-types' drops from M3 to M1", out)
        self.assertIn("stage 5: project brief 'briefs/missing.md' does not exist", out)

    def test_track_id_must_match_file_and_parent_must_exist(self):
        php = self._copy_tracks()
        (php.parent / "core.yaml").rename(php.parent / "kernel.yaml")
        code, out = self.repo.run()
        self.assertEqual(code, 1)
        self.assertIn("id 'core' must match the file name 'kernel'", out)


if __name__ == "__main__":
    unittest.main()
