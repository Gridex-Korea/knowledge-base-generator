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
            self.assertTrue((out / ".github/workflows/validate.yml").exists())
            self.assertTrue((out / "hubs/Topic Hub.md").exists())
            self.assertIn("해상풍력", (out / "README.md").read_text(encoding="utf-8"))
            proc = subprocess.run(
                [sys.executable, str(out / "scripts/validate_kb.py"), str(out)],
                capture_output=True,
                text=True,
            )
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)


if __name__ == "__main__":
    unittest.main()
