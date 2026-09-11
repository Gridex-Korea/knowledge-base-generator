from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from kb_generator.cli import ProjectSpec, generate
from kb_generator.ops import (
    audit_evidence,
    doctor,
    extract_grounding,
    github_bootstrap_plan,
    load_project,
    write_research_plan,
)
from kb_generator.router import main as router_main


class OperationsTest(unittest.TestCase):
    def make_kb(self, root: Path) -> Path:
        target = root / "offshore-wind-knowledge-base"
        spec = ProjectSpec(
            topic="해상풍력",
            name="해상풍력 Knowledge Base",
            slug="offshore-wind",
            kb_type="Technology / Policy / Industry",
            language="ko",
            countries=["KR", "AU"],
            site="quartz",
            gcp_level=2,
            public=True,
            created="2026-09-11",
        )
        generate(spec, target)
        return target

    def test_load_project_and_research_plan(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_kb(Path(tmp))
            project = load_project(root)
            self.assertEqual(project["topic"], "해상풍력")
            self.assertEqual(project["countries"], ["KR", "AU"])
            plan = write_research_plan(root)
            text = plan.read_text(encoding="utf-8")
            self.assertIn("Source-of-Truth map", text)
            self.assertIn("해상풍력", text)
            self.assertIn("Candidate Source", text)

    def test_audit_and_doctor(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_kb(Path(tmp))
            audit = audit_evidence(root)
            self.assertGreaterEqual(audit["notes"], 7)
            self.assertGreaterEqual(audit["unverified"], 1)
            self.assertTrue(Path(audit["report"]).exists())
            health = doctor(root)
            self.assertEqual(health["status"], "ok")
            self.assertEqual(health["validator_exit_code"], 0)

    def test_extract_grounding(self):
        response = {
            "candidates": [{
                "content": {"parts": [{"text": "Grounded summary"}]},
                "groundingMetadata": {
                    "webSearchQueries": ["official offshore wind Korea"],
                    "groundingChunks": [
                        {"web": {"uri": "https://example.go.kr/a", "title": "Official A", "domain": "example.go.kr"}},
                        {"web": {"uri": "https://example.go.kr/a", "title": "Duplicate", "domain": "example.go.kr"}},
                        {"web": {"uri": "https://example.org/b", "title": "Official B", "domain": "example.org"}},
                    ],
                },
            }]
        }
        text, queries, sources = extract_grounding(response)
        self.assertEqual(text, "Grounded summary")
        self.assertEqual(queries, ["official offshore wind Korea"])
        self.assertEqual(len(sources), 2)
        self.assertEqual(sources[0]["title"], "Official A")

    def test_github_bootstrap_is_dry_run_plan(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_kb(Path(tmp))
            plan = github_bootstrap_plan(root, owner="Uptec-khj")
            self.assertEqual(plan["target"], "Uptec-khj/offshore-wind-knowledge-base")
            self.assertTrue(any("gh repo create" in command for command in plan["commands"]))
            self.assertFalse(plan["private"])

    def test_router_backward_compatibility_and_commands(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "gfm-kb"
            code = router_main(["GFM", "-o", str(output), "--gcp-level", "0"])
            self.assertEqual(code, 0)
            self.assertTrue((output / "project.yaml").exists())
            self.assertEqual(router_main(["research", str(output)]), 0)
            self.assertEqual(router_main(["audit", str(output)]), 0)
            self.assertEqual(router_main(["doctor", str(output)]), 0)


if __name__ == "__main__":
    unittest.main()
