import io
import unittest
import zipfile

from kb_generator.web import spec_from_form, zip_project


class WebGeneratorTests(unittest.TestCase):
    def test_form_to_spec(self):
        spec = spec_from_form({
            "topic": ["해상풍력"],
            "countries": ["KR AU"],
            "gcp_level": ["2"],
            "site": ["quartz"],
        })
        self.assertEqual(spec.slug, "offshore-wind")
        self.assertEqual(spec.countries, ["KR", "AU"])
        self.assertEqual(spec.gcp_level, 2)

    def test_zip_contains_vault(self):
        spec = spec_from_form({
            "topic": ["HVDC"],
            "countries": ["KR"],
            "gcp_level": ["1"],
            "site": ["quartz"],
        })
        payload = zip_project(spec)
        with zipfile.ZipFile(io.BytesIO(payload)) as zf:
            names = set(zf.namelist())
        prefix = "hvdc-knowledge-base/"
        dev_prefix = "hvdc-knowledge-base-dev/"
        self.assertEqual({name.split("/")[0] for name in names}, {"hvdc-knowledge-base", "hvdc-knowledge-base-dev"})
        self.assertIn(dev_prefix + "sources/README.md", names)
        self.assertIn(dev_prefix + "data/source-archive.yaml", names)
        self.assertIn(dev_prefix + "project/roadmap.md", names)
        self.assertNotIn(prefix + "project/roadmap.md", names)
        self.assertNotIn(prefix + "data/source-archive.yaml", names)
        self.assertIn(prefix + "HOME.md", names)
        self.assertIn(prefix + "project.yaml", names)
        self.assertIn(prefix + "scripts/validate_kb.py", names)


if __name__ == "__main__":
    unittest.main()
