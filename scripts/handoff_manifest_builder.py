"""Build a handoff file manifest and check required package artifacts."""

from __future__ import annotations

import argparse
import csv
import sys
from datetime import datetime
from pathlib import Path


REQUIRED_HINTS = [
    "tables",
    "figures",
    "logs",
    "do",
    "variable_map",
    "table_inventory",
    "sample_flow",
    "evidence_map",
    "regression_run_report",
    "failed_regressions",
    "P0_status",
    "P1_risks",
    "final_regression_audit",
    "handoff_README",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create file_manifest.csv for a handoff package.")
    parser.add_argument("--handoff-dir", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--fail-on-missing-required", action="store_true")
    return parser.parse_args()


def has_hint(files: list[Path], hint: str) -> bool:
    h = hint.lower()
    if h == "do":
        return any(p.suffix.lower() == ".do" for p in files)
    return any(h in str(p).lower() for p in files)


def main() -> int:
    args = parse_args()
    if not args.handoff_dir.exists():
        print(f"P0: handoff directory does not exist: {args.handoff_dir}", file=sys.stderr)
        return 2
    files = [p for p in args.handoff_dir.rglob("*") if p.is_file()]
    missing = [hint for hint in REQUIRED_HINTS if not has_hint(files, hint)]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["file_path", "size_bytes", "modified_time", "required_check_status"])
        writer.writeheader()
        for file in sorted(files):
            writer.writerow(
                {
                    "file_path": str(file),
                    "size_bytes": file.stat().st_size,
                    "modified_time": datetime.fromtimestamp(file.stat().st_mtime).isoformat(timespec="seconds"),
                    "required_check_status": "present",
                }
            )
        for hint in missing:
            writer.writerow(
                {
                    "file_path": f"REQUIRED_MISSING:{hint}",
                    "size_bytes": "",
                    "modified_time": "",
                    "required_check_status": "P0_MISSING_REQUIRED",
                }
            )
    print(f"Wrote handoff manifest to {args.output}")
    if missing:
        print("Missing required handoff artifacts: " + ", ".join(missing), file=sys.stderr)
    return 1 if missing and args.fail_on_missing_required else 0


if __name__ == "__main__":
    raise SystemExit(main())
