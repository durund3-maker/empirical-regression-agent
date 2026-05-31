"""Validate sample-flow records for auditable sample changes."""

from __future__ import annotations

import argparse
import csv
import sys
from datetime import datetime
from pathlib import Path


SAMPLE_ACTIONS = {"drop", "keep", "merge", "deduplicate", "winsorize", "trim", "outlier handling", "outlier_handling"}
REQUIRED_FIELDS = ["before_n", "after_n", "delta_n", "decision_source", "author_confirmed"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check sample_flow.csv for unconfirmed sample changes.")
    parser.add_argument("--sample-flow", required=True, type=Path)
    parser.add_argument("--output", type=Path, help="Markdown report. Defaults to stdout.")
    parser.add_argument("--fail-on-p0", action="store_true")
    return parser.parse_args()


def truthy(value: str) -> bool:
    return str(value).strip().lower() in {"true", "yes", "1", "approved", "confirmed"}


def main() -> int:
    args = parse_args()
    if not args.sample_flow.exists():
        print(f"P0: sample_flow file does not exist: {args.sample_flow}", file=sys.stderr)
        return 2
    with args.sample_flow.open("r", newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    p0: list[str] = []
    for idx, row in enumerate(rows, start=2):
        action = (row.get("action") or row.get("step_type") or row.get("operation") or "").strip().lower()
        if action not in SAMPLE_ACTIONS:
            continue
        missing = [field for field in REQUIRED_FIELDS if not row.get(field)]
        if missing:
            p0.append(f"line {idx}: {action} missing {', '.join(missing)}")
        if not truthy(row.get("author_confirmed", "")):
            p0.append(f"line {idx}: {action} is not author confirmed")
    lines = [
        "# Sample Flow Check",
        "",
        f"- Generated: {datetime.now().isoformat(timespec='seconds')}",
        f"- Sample flow: `{args.sample_flow}`",
        "- Scope: validation only; sample flow was not modified.",
        "",
        "## P0 Findings",
        "",
    ]
    lines += [f"- {item}" for item in p0] if p0 else ["No P0 sample-flow findings detected."]
    report = "\n".join(lines) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report, encoding="utf-8")
    else:
        print(report)
    return 1 if p0 and args.fail_on_p0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
