from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from kb_generator.cli import ProjectSpec, generate, infer_type, slugify


class GeneratorTests(unittest.TestCase):
    def test_known_korean_slug(self):
        self.assertEqual(slugify("해상풍력"), "offshore-wind")
        self.assertEqual(slugify("수소산업"), "hydrogen-industry")

    def test_ascii_slug(self):
        self.assertEqual(slugify("Power Market Rules"), "power-market-rules")

    def test_unknown_korean_has_stable_fallback(self):
        self.assertTrue(slugify("새로운분야").startswith("knowledge-base-"))
        self.assertEqual(slugify("새로운분야"), slugify("새로운분야"))

    def test_type_inference(self):
        self.assertIn("Procurement", infer_type("전력입찰"))
        self.assertIn("Technology", infer_type("HVDC"))

    def test_generate_builtin_and_validate(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "out"
            spec = ProjectSpec(
                "해상풍력",
                "해상풍력 Knowledge Base",
                "offshore-wind",
                "Mixed",
                "ko",
                ["KR"],
                "quartz",
                1,
                True,
                "2026-09-11",
            )
            generate(spec, out)
            self.assertTrue((out / "project.yaml").exists())
            dev = out.with_name("out-dev")
            self.assertTrue((dev / "sources/README.md").exists())
            self.assertTrue((dev / "data/source-archive.yaml").exists())
            self.assertTrue((dev / "project/roadmap.md").exists())
            self.assertFalse((out / "project").exists())
            self.assertFalse((out / "sources").exists())
            self.assertIn('development_repository: "out-dev"', (out / "project.yaml").read_text(encoding="utf-8"))
            self.assertNotIn("sources", (dev / ".gitignore").read_text(encoding="utf-8"))
            self.assertTrue((out / ".github/workflows/validate.yml").exists())
            self.assertTrue((out / "hubs/Topic Hub.md").exists())
            self.assertIn("해상풍력", (out / "README.md").read_text(encoding="utf-8"))
            proc = subprocess.run(
                [sys.executable, str(out / "scripts/validate_kb.py"), str(out)],
                capture_output=True,
                text=True,
            )
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            (out / "sources").mkdir()
            (out / "sources/original.txt").write_text("original text", encoding="utf-8")
            rejected = subprocess.run([sys.executable, str(out / "scripts/validate_kb.py"), str(out)], capture_output=True, text=True)
            self.assertEqual(rejected.returncode, 1)
            self.assertIn("private <name>-dev", rejected.stdout)

    def test_private_only_and_unsafe_slug_rejected_without_files(self):
        for public, slug in ((False, "hvdc"), (True, "../../outside")):
            with self.subTest(public=public, slug=slug), tempfile.TemporaryDirectory() as td:
                out = Path(td) / "kb"
                spec = ProjectSpec("HVDC", "HVDC", slug, "Mixed", "ko", ["KR"], "quartz", 0, public, "2026-09-12")
                with self.assertRaises(ValueError):
                    generate(spec, out)
                self.assertFalse(out.exists())

    def test_development_collision_does_not_partially_generate(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "kb"
            dev = Path(td) / "kb-dev"
            dev.mkdir()
            (dev / "existing.txt").write_text("keep")
            spec = ProjectSpec("HVDC", "HVDC", "hvdc", "Mixed", "ko", [], "none", 0, True, "2026-09-12")
            with self.assertRaises(FileExistsError):
                generate(spec, out)
            self.assertFalse(out.exists())
            self.assertEqual((dev / "existing.txt").read_text(), "keep")

    def test_force_preserves_archived_source_provenance(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "custom-kb"
            spec = ProjectSpec("HVDC", "HVDC", "hvdc", "Mixed", "ko", [], "none", 0, True, "2026-09-12")
            generate(spec, out)
            dev = out.with_name("custom-kb-dev")
            archive = dev / "data/source-archive.yaml"
            original = dev / "sources/original.txt"
            archive.write_text("version: 1\narchives: [existing]\n", encoding="utf-8")
            original.write_text("original", encoding="utf-8")
            generate(spec, out, force=True)
            self.assertIn("existing", archive.read_text(encoding="utf-8"))
            self.assertEqual(original.read_text(encoding="utf-8"), "original")
            self.assertIn("REPLACE_WITH_OWNER/custom-kb-dev", (dev / "gcp/config.yaml").read_text(encoding="utf-8"))

    def test_custom_template_private_sources_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            template = Path(td) / "template"
            (template / "sources").mkdir(parents=True)
            spec = ProjectSpec("HVDC", "HVDC", "hvdc", "Mixed", "ko", [], "none", 0, True, "2026-09-12")
            with self.assertRaises(ValueError):
                generate(spec, Path(td) / "kb", template)


if __name__ == "__main__":
    unittest.main()
