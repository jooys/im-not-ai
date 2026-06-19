#!/usr/bin/env python3
"""Run the Korean humanize pilot gate over fixture/output pairs."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

# Allow running as `python scripts/qa_humanize_gate.py`.
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from check_humanize_output import validate  # noqa: E402


def write_report(results: list[dict], report_path: Path) -> None:
    total = len(results)
    passed = sum(1 for r in results if r["contract_status"] == "PASS")
    failed = total - passed
    critical_fail_zero = failed == 0

    lines = [
        "# Korean Humanize Editor Pilot QA Report",
        "",
        "## Summary",
        "",
        f"- Total fixtures: {total}",
        f"- Contract PASS: {passed}",
        f"- Contract FAIL: {failed}",
        f"- Critical fail zero: {'YES' if critical_fail_zero else 'NO'}",
        "",
        "## Fixture Results",
        "",
        "| Fixture | Expected | Actual | Contract | Change rate | Notes |",
        "|---|---|---|---|---:|---|",
    ]
    for r in results:
        notes = []
        if r["errors"]:
            notes.append("errors: " + "; ".join(r["errors"]))
        if r["warnings"]:
            notes.append("warnings: " + "; ".join(r["warnings"]))
        notes_text = "<br>".join(notes) if notes else "-"
        lines.append(
            f"| {r['fixture_id']} | {r['expected_status']} | {r['actual_status']} | "
            f"{r['contract_status']} | {r['change_rate']:.2f}% | {notes_text} |"
        )
    lines.extend(
        [
            "",
            "## Gate Decision",
            "",
            "PASS" if critical_fail_zero else "FAIL",
            "",
            "## Scope",
            "",
            "This report checks deterministic safety contracts only. It does not prove subjective writing quality. Human review is still required before cross-profile rollout.",
            "",
        ]
    )
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixtures", required=True, type=Path)
    parser.add_argument("--outputs", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    args = parser.parse_args()

    fixture_paths = sorted(args.fixtures.glob("*.json"))
    if not fixture_paths:
        print(f"no fixtures found under {args.fixtures}", file=sys.stderr)
        return 1

    results: list[dict] = []
    for fixture_path in fixture_paths:
        fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
        output_path = args.outputs / f"{fixture['id']}.md"
        if not output_path.is_file():
            results.append(
                {
                    "fixture_id": fixture["id"],
                    "expected_status": fixture.get("expected_status", "PASS"),
                    "actual_status": "MISSING",
                    "contract_status": "FAIL",
                    "change_rate": 0.0,
                    "errors": [f"missing output file: {output_path}"],
                    "warnings": [],
                }
            )
            continue
        result = validate(fixture, output_path.read_text(encoding="utf-8"))
        results.append(asdict(result))

    write_report(results, args.report)
    for r in results:
        print(
            f"{r['fixture_id']}: contract={r['contract_status']} "
            f"expected={r['expected_status']} actual={r['actual_status']} "
            f"change_rate={r['change_rate']:.2f}%"
        )
        for error in r["errors"]:
            print(f"ERROR {r['fixture_id']}: {error}", file=sys.stderr)
        for warning in r["warnings"]:
            print(f"WARN {r['fixture_id']}: {warning}")

    return 0 if all(r["contract_status"] == "PASS" for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
