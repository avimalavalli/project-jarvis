#!/usr/bin/env python3
"""Validate Phase 0 repository controls without network access or dependencies."""

from __future__ import annotations

import json
import re
import sys
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = (
    "README.md",
    "SECURITY.md",
    "CHANGELOG.md",
    ".github/CODEOWNERS",
    ".github/workflows/phase0.yml",
    "docs/blueprint/README.md",
    "docs/phase-checklists/phase-0.md",
    "docs/architecture/service-boundaries.md",
    "docs/architecture/ownership-map.md",
    "docs/architecture/model-routing-v1.md",
    "docs/architecture/upstream-boundary.md",
    "docs/architecture/device-endpoint-v1.md",
    "docs/persona/constitution-v1.md",
    "docs/memory/world-model-v1.md",
    "docs/adr/0000-template.md",
    "docs/adr/0001-foundation-strategy.md",
    "docs/adr/0002-public-source-boundary.md",
    "docs/security/permission-taxonomy-v1.md",
    "docs/security/threat-model.md",
    "docs/security/data-classification.md",
    "docs/risks/REGISTER.md",
    "docs/runbooks/backup-recovery.md",
    "docs/runbooks/actual-pc-assessment.md",
    "foundation/openjarvis/PIN.json",
    "foundation/openjarvis/PATCHES.md",
    "foundation/openjarvis/EVALUATION.md",
    "config/evaluation/openjarvis-policy.toml",
    "config/dev/jarvis.toml",
    "config/staging/jarvis.toml",
    "config/production/jarvis.toml",
    "evals/golden/scenarios.json",
    "scripts/windows/collect_pc_inventory.ps1",
    "scripts/assess_openjarvis_source.py",
)

SECRET_PATTERNS = {
    "OpenAI-style key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
}


def validate_required_files() -> list[str]:
    return [f"missing required file: {path}" for path in REQUIRED_FILES if not (ROOT / path).is_file()]


def validate_json() -> list[str]:
    errors: list[str] = []
    for path in sorted((ROOT / "contracts").glob("*.schema.json")):
        try:
            document = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"invalid JSON {path.relative_to(ROOT)}: {exc}")
            continue
        if document.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            errors.append(f"unexpected JSON Schema dialect: {path.relative_to(ROOT)}")
    if len(list((ROOT / "contracts").glob("*.schema.json"))) != 7:
        errors.append("expected exactly seven Phase 0 contract schemas")
    return errors


def validate_policy() -> list[str]:
    path = ROOT / "config/evaluation/openjarvis-policy.toml"
    with path.open("rb") as handle:
        policy = tomllib.load(handle)
    checks = {
        "Phase 1 must remain unauthorised": policy["phase"]["phase_1_authorized"] is False,
        "evaluation host must be loopback": policy["network"]["host"] == "127.0.0.1",
        "remote access must be disabled": policy["network"]["allow_remote"] is False,
        "external telemetry must be disabled": policy["telemetry"]["external_enabled"] is False,
        "tools must default deny": policy["tools"]["default_policy"] == "deny",
        "no tools may be enabled": policy["tools"]["enabled"] == [],
        "cloud models must be disabled": policy["models"]["allow_cloud"] is False,
        "paid keys must not be required": policy["models"]["paid_key_required"] is False,
        "automatic memory capture must be disabled": policy["memory"]["automatic_capture"] is False,
        "plaintext secrets must be disabled": policy["secrets"]["allow_plaintext_files"] is False,
    }
    return [message for message, passed in checks.items() if not passed]


def validate_pin() -> list[str]:
    pin = json.loads((ROOT / "foundation/openjarvis/PIN.json").read_text(encoding="utf-8"))
    errors: list[str] = []
    if pin["selected"] is not None:
        errors.append("OpenJarvis must remain unselected until evaluation evidence exists")
    if pin["patch_count"] != 0:
        errors.append("initial upstream patch count must be zero")
    for candidate in pin["candidates"]:
        sha = candidate.get("resolved_commit_sha")
        if not isinstance(sha, str) or not re.fullmatch(r"[0-9a-f]{40}", sha):
            errors.append(f"candidate is not resolved to an exact SHA: {candidate.get('name')}")
    return errors


def validate_environments() -> list[str]:
    errors: list[str] = []
    expected = {"dev": False, "staging": False, "production": True}
    for name, production in expected.items():
        path = ROOT / "config" / name / "jarvis.toml"
        with path.open("rb") as handle:
            config = tomllib.load(handle)
        checks = {
            "environment name": config["environment"]["name"] == name,
            "production flag": config["environment"]["production"] is production,
            "loopback host": config["network"]["host"] == "127.0.0.1",
            "remote disabled": config["network"]["allow_remote"] is False,
            "external telemetry disabled": config["telemetry"]["external_enabled"] is False,
            "tools default deny": config["tools"]["default_policy"] == "deny",
            "tools empty": config["tools"]["enabled"] == [],
            "cloud disabled": config["models"]["allow_cloud"] is False,
            "automatic memory disabled": config["memory"]["automatic_capture"] is False,
            "plaintext secrets disabled": config["secrets"]["allow_plaintext_files"] is False,
        }
        errors.extend(f"{name}: {label}" for label, passed in checks.items() if not passed)
    return errors


def validate_golden_scenarios() -> list[str]:
    path = ROOT / "evals/golden/scenarios.json"
    document = json.loads(path.read_text(encoding="utf-8"))
    scenarios = document.get("scenarios", [])
    ids = [scenario.get("id") for scenario in scenarios]
    errors: list[str] = []
    if len(scenarios) < 12:
        errors.append("golden suite must contain at least 12 scenarios")
    if len(ids) != len(set(ids)):
        errors.append("golden scenario IDs must be unique")
    required_categories = {"identity", "truthfulness", "permissions", "routing", "memory", "privacy", "actions", "injection", "devices"}
    present = {scenario.get("category") for scenario in scenarios}
    missing = sorted(required_categories - present)
    if missing:
        errors.append(f"golden suite missing categories: {', '.join(missing)}")
    return errors


def validate_inventory_privacy() -> list[str]:
    text = (ROOT / "scripts/windows/collect_pc_inventory.ps1").read_text(encoding="utf-8")
    prohibited = ("Win32_UserAccount", "UserName", "SerialNumber", "IPAddress", "Get-ChildItem Env:")
    return [f"inventory script contains prohibited collection token: {token}" for token in prohibited if token in text]


def validate_ci_supply_chain() -> list[str]:
    text = (ROOT / ".github/workflows/phase0.yml").read_text(encoding="utf-8")
    action_refs = re.findall(r"uses:\s+[^@\s]+@([^\s#]+)", text)
    return [f"GitHub Action is not pinned to a full SHA: {ref}" for ref in action_refs if not re.fullmatch(r"[0-9a-f]{40}", ref)]


def scan_for_secrets() -> list[str]:
    errors: list[str] = []
    suffixes = {".md", ".py", ".toml", ".json", ".yml", ".yaml"}
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in suffixes or ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"possible {label} in {path.relative_to(ROOT)}")
    return errors


def main() -> int:
    errors = [
        *validate_required_files(),
        *validate_json(),
        *validate_policy(),
        *validate_pin(),
        *validate_environments(),
        *validate_golden_scenarios(),
        *validate_inventory_privacy(),
        *validate_ci_supply_chain(),
        *scan_for_secrets(),
    ]
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print("PASS: Phase 0 foundation controls are internally consistent.")
    print("NOTE: Phase 0 exit gates remain open; this check does not authorise Phase 1.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
