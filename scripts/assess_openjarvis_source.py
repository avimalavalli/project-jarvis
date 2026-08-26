#!/usr/bin/env python3
"""Inspect an OpenJarvis checkout without importing or executing its code."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tomllib
from datetime import datetime, timezone
from pathlib import Path


REQUIRED_AREAS = ("engine", "security", "tools")
OBSERVED_AREAS = (*REQUIRED_AREAS, "memory")


def git(source: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(source), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def assess(source: Path, expected_sha: str) -> dict[str, object]:
    head = git(source, "rev-parse", "HEAD")
    dirty = bool(git(source, "status", "--porcelain"))
    pyproject_path = source / "pyproject.toml"
    pyproject: dict[str, object] = {}
    pyproject_error: str | None = None
    if pyproject_path.is_file():
        try:
            pyproject = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
        except (OSError, tomllib.TOMLDecodeError) as exc:
            pyproject_error = str(exc)
    package_roots = (source / "src" / "openjarvis", source / "openjarvis")
    package_root = next((path for path in package_roots if path.is_dir()), package_roots[0])
    areas = {name: (package_root / name).is_dir() for name in OBSERVED_AREAS}
    checks = {
        "head_matches": head == expected_sha,
        "tree_clean": not dirty,
        "pyproject_present": pyproject_path.is_file(),
        "pyproject_parseable": pyproject_error is None,
        "package_present": package_root.is_dir(),
        "required_areas_present": all(areas[name] for name in REQUIRED_AREAS),
    }
    return {
        "schema_version": "1.0",
        "collected_at_utc": datetime.now(timezone.utc).isoformat(),
        "source": str(source.resolve()),
        "expected_sha": expected_sha,
        "head_sha": head,
        "python_requires": pyproject.get("project", {}).get("requires-python"),
        "pyproject_error": pyproject_error,
        "package_root": str(package_root.relative_to(source)),
        "areas": areas,
        "checks": checks,
        "passed": all(checks.values()),
        "scope": "Source identity only; no OpenJarvis code was imported or executed.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--expected-sha", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = assess(args.source, args.expected_sha)
    rendered = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
