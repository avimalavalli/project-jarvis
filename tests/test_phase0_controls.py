from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("check_phase0", ROOT / "scripts/check_phase0.py")
assert SPEC and SPEC.loader
CHECKS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKS)


class Phase0ControlTests(unittest.TestCase):
    def test_required_files_exist(self) -> None:
        self.assertEqual(CHECKS.validate_required_files(), [])

    def test_contract_schemas_are_valid_json(self) -> None:
        self.assertEqual(CHECKS.validate_json(), [])

    def test_evaluation_policy_fails_closed(self) -> None:
        self.assertEqual(CHECKS.validate_policy(), [])

    def test_upstream_is_not_prematurely_selected_or_patched(self) -> None:
        self.assertEqual(CHECKS.validate_pin(), [])

    def test_environment_profiles_fail_closed(self) -> None:
        self.assertEqual(CHECKS.validate_environments(), [])

    def test_golden_suite_covers_foundation_risks(self) -> None:
        self.assertEqual(CHECKS.validate_golden_scenarios(), [])

    def test_pc_inventory_avoids_private_identifiers(self) -> None:
        self.assertEqual(CHECKS.validate_inventory_privacy(), [])

    def test_windows_candidate_harness_fails_closed(self) -> None:
        self.assertEqual(CHECKS.validate_windows_candidate_harness(), [])

    def test_windows_version_probes_avoid_pipeline_exit_state(self) -> None:
        harness = (ROOT / "scripts/windows/evaluate_openjarvis_candidates.ps1").read_text(
            encoding="utf-8"
        ).lower()
        version_section = harness.split("$git = get-requiredapplication", 1)[-1].split(
            "$pin =", 1
        )[0]
        self.assertNotIn("$lastexitcode", version_section)

    def test_ci_actions_are_sha_pinned(self) -> None:
        self.assertEqual(CHECKS.validate_ci_supply_chain(), [])

    def test_no_obvious_secret_material_is_committed(self) -> None:
        self.assertEqual(CHECKS.scan_for_secrets(), [])


if __name__ == "__main__":
    unittest.main()
