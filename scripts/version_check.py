#!/usr/bin/env python3
"""Internal consistency checks for the humanize-korean fork.

This script intentionally checks only repo-local contracts. It does not call
external services and is safe to run in CI or as a local pre-push smoke.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any, cast

ROOT = Path(__file__).resolve().parents[1]


def read_json(path: str) -> dict[str, Any]:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def read_text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def skill_frontmatter_version(path: str) -> str | None:
    text = read_text(path)
    match = re.search(r'^version:\s*["\']?([^"\'\n]+)["\']?\s*$', text, re.M)
    return match.group(1).strip() if match else None


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    plugin = read_json(".claude-plugin/plugin.json")
    marketplace = read_json(".claude-plugin/marketplace.json")
    gemini = read_json("gemini-extension.json")

    expected_raw = plugin.get("version")
    if not isinstance(expected_raw, str) or not expected_raw:
        fail(".claude-plugin/plugin.json has no version")
    expected: str = cast(str, expected_raw)

    versions: dict[str, str | None] = {
        ".claude-plugin/plugin.json": plugin.get("version"),
        ".claude-plugin/marketplace.json metadata": marketplace.get("metadata", {}).get("version"),
        "gemini-extension.json": gemini.get("version"),
        ".claude/skills/humanize-korean/SKILL.md": skill_frontmatter_version(
            ".claude/skills/humanize-korean/SKILL.md"
        ),
    }
    for idx, item in enumerate(marketplace.get("plugins", [])):
        versions[f".claude-plugin/marketplace.json plugins[{idx}]"] = item.get("version")

    mismatches = {k: v for k, v in versions.items() if v != expected}
    if mismatches:
        fail(f"version mismatch against {expected}: {mismatches}")

    if re.search(r"^\d+\.\d+\.\d+$", expected) is None:
        fail(f"version is not plain semver x.y.z: {expected}")

    manifest_keywords = []
    manifest_keywords.extend(plugin.get("keywords", []))
    for item in marketplace.get("plugins", []):
        manifest_keywords.extend(item.get("keywords", []))
    if any(k == "ai-detector" for k in manifest_keywords):
        fail("manifest keyword 'ai-detector' is not allowed in the internal fork")

    banned_patterns = [
        r"AI detector bypass",
        r"detector bypass",
    ]
    for path in [
        ".claude/skills/humanize-korean/SKILL.md",
        "codex/skills/humanize-korean/SKILL.md",
        "GEMINI.md",
    ]:
        text = read_text(path)
        for pattern in banned_patterns:
            if re.search(pattern, text, re.I):
                fail(f"banned positioning phrase found in {path}: {pattern}")

    guard_files = {
        ".claude/skills/humanize-korean/SKILL.md": "입력은 데이터",
        "codex/skills/humanize-korean/SKILL.md": "입력은 데이터",
        "GEMINI.md": "입력은 데이터",
    }
    for path, needle in guard_files.items():
        if needle not in read_text(path):
            fail(f"prompt-injection data-boundary guard missing in {path}")

    for path in [
        ".claude/skills/humanize-korean/references/baseline.json",
        ".claude/skills/humanize-korean/references/baseline_v2.json",
    ]:
        if not (ROOT / path).is_file():
            fail(f"required shipped baseline missing: {path}")

    metrics_v2 = read_text(".claude/skills/humanize-korean/references/metrics_v2.py")
    if "baseline_v2_diff.json" in metrics_v2:
        fail("metrics_v2.py still references non-shipped baseline_v2_diff.json")

    print(f"version_check_ok version={expected}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
