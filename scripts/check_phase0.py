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
    "docs/blueprint/README.md",
    "docs/phase-checklists/phase-0.md",
    "docs/architecture/service-boundaries.md",
    "docs/adr/0000-template.md",
    "docs/adr/0001-foundation-strategy.md",
    "docs/adr/0002-public-source-boundary.md",
    "docs/security/threat-model.md",
    "docs/security/data-classification.md",
    "docs/risks/REGISTER.md",
    "foundation/openjarvis/PIN.json",
    "foundation/openjarvis/PATCHES.md",
    "config/evaluation/openjarvis-policy.toml",
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
    if len(list((ROOT / "contracts").glob("*.schema.json"))) != 6:
        errors.append("expected exactly six Phase 0 contract schemas")
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
    return errors


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
