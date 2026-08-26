from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "assess_openjarvis_source", ROOT / "scripts/assess_openjarvis_source.py"
)
assert SPEC and SPEC.loader
ASSESSOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ASSESSOR)


class OpenJarvisSourceAssessmentTests(unittest.TestCase):
    def test_assessment_checks_identity_without_importing_upstream(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory)
            (source / "src" / "openjarvis").mkdir(parents=True)
            for area in ASSESSOR.OBSERVED_AREAS:
                (source / "src" / "openjarvis" / area).mkdir()
            (source / "pyproject.toml").write_text(
                '[project]\nname = "openjarvis"\nrequires-python = ">=3.10,<3.14"\n',
                encoding="utf-8",
            )
            with patch.object(ASSESSOR, "git", side_effect=["a" * 40, ""]):
                report = ASSESSOR.assess(source, "a" * 40)
            self.assertTrue(report["passed"])
            self.assertIn("no OpenJarvis code was imported", report["scope"])


if __name__ == "__main__":
    unittest.main()
