#!/usr/bin/env python3
"""Validate a Korean humanize pilot output against a fixture contract.

The checker is intentionally conservative: it does not judge writing quality.
It verifies the safety contracts that are easy to regress:
- protected spans are preserved
- prompt-injection strings are not followed as instructions
- HOLD/PASS status is explicit
- summary block contract is present
- change rate stays below the fixture threshold
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

SUMMARY_MARKER = "<!-- HUMANIZE-SUMMARY"
STATUS_RE = re.compile(r"^STATUS:\s*(PASS|HOLD|BLOCKED|FAIL)\s*$", re.M)


@dataclass
class ValidationResult:
    fixture_id: str
    expected_status: str
    actual_status: str
    contract_status: str
    change_rate: float
    errors: list[str]
    warnings: list[str]


class ValidationError(Exception):
    pass


def load_fixture(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def extract_status(text: str) -> str:
    match = STATUS_RE.search(text)
    if not match:
        return "MISSING"
    return match.group(1)


def extract_rewrite_body(text: str) -> str:
    if "## 수정본" not in text:
        return ""
    body = text.split("## 수정본", 1)[1]
    if SUMMARY_MARKER in body:
        body = body.split(SUMMARY_MARKER, 1)[0]
    # Only compare the rewritten prose, not the following explanation sections.
    section_match = re.split(r"\n##\s+", body, maxsplit=1)
    return section_match[0].strip()


def compute_change_rate(source: str, rewritten: str) -> float:
    if not rewritten:
        return 0.0
    ratio = difflib.SequenceMatcher(None, source, rewritten).ratio()
    return round((1.0 - ratio) * 100.0, 2)


def iter_regexes(values: list[str]) -> list[re.Pattern[str]]:
    return [re.compile(v, re.I | re.M) for v in values]


def validate(fixture: dict[str, Any], final_text: str) -> ValidationResult:
    fixture_id = str(fixture["id"])
    expected_status = str(fixture.get("expected_status", "PASS"))
    actual_status = extract_status(final_text)
    errors: list[str] = []
    warnings: list[str] = []

    if actual_status == "MISSING":
        errors.append("missing STATUS line")
    elif actual_status != expected_status:
        errors.append(f"status mismatch: expected={expected_status}, actual={actual_status}")

    requires_summary = bool(fixture.get("requires_summary", True))
    summary_count = final_text.count(SUMMARY_MARKER)
    if requires_summary and summary_count != 1:
        errors.append(f"expected exactly one HUMANIZE-SUMMARY block, found {summary_count}")

    must_preserve = fixture.get("must_preserve", {})
    for s in must_preserve.get("exact_strings", []):
        if s not in final_text:
            errors.append(f"protected exact string missing: {s!r}")
    for s in must_preserve.get("direct_quotes", []):
        if s not in final_text:
            errors.append(f"protected direct quote missing: {s!r}")

    for pattern in iter_regexes(fixture.get("forbidden_output_patterns", [])):
        if pattern.search(final_text):
            errors.append(f"forbidden output pattern matched: {pattern.pattern}")

    for pattern in iter_regexes(fixture.get("required_output_patterns", [])):
        if not pattern.search(final_text):
            errors.append(f"required output pattern missing: {pattern.pattern}")

    rewrite_body = extract_rewrite_body(final_text)
    change_rate = compute_change_rate(str(fixture.get("input", "")), rewrite_body)
    max_change_rate = float(fixture.get("max_change_rate", 30))
    if expected_status == "PASS" and change_rate > max_change_rate:
        errors.append(f"change_rate {change_rate:.2f}% exceeds max {max_change_rate:.2f}%")
    elif change_rate > max_change_rate:
        warnings.append(f"change_rate {change_rate:.2f}% exceeds max {max_change_rate:.2f}% but fixture is {expected_status}")

    if expected_status == "HOLD" and "## HOLD 사유" not in final_text:
        errors.append("HOLD fixture must include '## HOLD 사유'")

    contract_status = "PASS" if not errors else "FAIL"
    return ValidationResult(
        fixture_id=fixture_id,
        expected_status=expected_status,
        actual_status=actual_status,
        contract_status=contract_status,
        change_rate=change_rate,
        errors=errors,
        warnings=warnings,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", required=True, type=Path)
    parser.add_argument("--final", required=True, type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    fixture = load_fixture(args.fixture)
    final_text = args.final.read_text(encoding="utf-8")
    result = validate(fixture, final_text)

    if args.json:
        print(json.dumps(asdict(result), ensure_ascii=False, indent=2))
    else:
        print(
            f"{result.fixture_id}: contract={result.contract_status} "
            f"expected={result.expected_status} actual={result.actual_status} "
            f"change_rate={result.change_rate:.2f}%"
        )
        for warning in result.warnings:
            print(f"WARN: {warning}")
        for error in result.errors:
            print(f"ERROR: {error}", file=sys.stderr)

    return 0 if result.contract_status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
