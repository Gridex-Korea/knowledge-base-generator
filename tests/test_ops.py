from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from subprocess import CompletedProcess

from kb_generator.repositories import development_root

from kb_generator.cli import ProjectSpec, generate
from kb_generator.ops import (
    audit_evidence,
    doctor,
    extract_grounding,
    github_bootstrap_plan,
    execute_github_bootstrap,
    _existing_origin,
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
            self.assertEqual(plan.parent, development_root(root) / "project")
            self.assertFalse((root / "project").exists())
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
            self.assertEqual([(r["target"], r["private"]) for r in plan["repositories"]], [
                ("Uptec-khj/offshore-wind-knowledge-base-dev", True),
                ("Uptec-khj/offshore-wind-knowledge-base", False),
            ])
            with self.assertRaises(RuntimeError):
                github_bootstrap_plan(root, private=True)

    def test_router_backward_compatibility_and_commands(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "gfm-kb"
            code = router_main(["GFM", "-o", str(output), "--gcp-level", "0"])
            self.assertEqual(code, 0)
            self.assertTrue((output / "project.yaml").exists())
            self.assertEqual(router_main(["research", str(output)]), 0)
            self.assertEqual(router_main(["audit", str(output)]), 0)
            self.assertEqual(router_main(["doctor", str(output)]), 0)

    def test_execute_creates_two_repositories_with_required_visibility(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_kb(Path(tmp))
            def run(args, **kwargs):
                code = 1 if args[1:4] == ["diff", "--cached", "--quiet"] else 0
                return CompletedProcess(args, code, "", "")
            with patch("kb_generator.ops.shutil.which", return_value="available"), patch("kb_generator.ops.subprocess.run", side_effect=run) as mocked:
                execute_github_bootstrap(root, owner="Uptec-khj")
            creates = [call for call in mocked.call_args_list if call.args[0][:3] == ["gh", "repo", "create"]]
            self.assertEqual(len(creates), 2)
            self.assertIn("--private", creates[0].args[0])
            self.assertTrue(creates[0].args[0][3].endswith("-dev"))
            self.assertEqual(creates[0].kwargs["cwd"], development_root(root))
            self.assertIn("--public", creates[1].args[0])
            self.assertEqual(creates[1].kwargs["cwd"], root)

    def test_public_source_directory_blocks_all_pushes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_kb(Path(tmp))
            (root / "sources").mkdir()
            with patch("kb_generator.ops.shutil.which", return_value="available"), patch("kb_generator.ops.subprocess.run") as mocked:
                with self.assertRaises(RuntimeError):
                    execute_github_bootstrap(root, owner="Uptec-khj")
                mocked.assert_not_called()

    def test_existing_development_origin_must_be_private(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".git").mkdir()
            target = "Uptec-khj/kb-dev"
            responses = [CompletedProcess([], 0, f"https://github.com/{target}.git\n", ""),
                         CompletedProcess([], 0, f"https://github.com/{target}.git\n", ""),
                         CompletedProcess([], 0, json.dumps({"nameWithOwner": target, "isPrivate": False}), "")]
            with patch("kb_generator.ops.subprocess.run", side_effect=responses):
                with self.assertRaisesRegex(RuntimeError, "visibility mismatch"):
                    _existing_origin(root, target, True)

    def test_doctor_reports_missing_development_repository(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_kb(Path(tmp))
            (development_root(root) / "repository.json").unlink()
            self.assertEqual(doctor(root)["status"], "needs-attention")
            with self.assertRaises(RuntimeError):
                github_bootstrap_plan(root)


if __name__ == "__main__":
    unittest.main()
