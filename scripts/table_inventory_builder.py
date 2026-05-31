"""Build an inventory of exported tables without reading or editing table numbers."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime
from pathlib import Path


TABLE_EXTENSIONS = {".rtf", ".tex", ".csv", ".xlsx"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create table_inventory.csv from exported table files.")
    parser.add_argument("--tables-dir", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--spec-file", type=Path)
    parser.add_argument("--logs-dir", type=Path)
    parser.add_argument("--do-dir", type=Path)
    return parser.parse_args()


def candidates(directory: Path, suffixes: set[str]) -> list[Path]:
    if not directory or not directory.exists():
        return []
    return [p for p in directory.rglob("*") if p.is_file() and p.suffix.lower() in suffixes]


def infer_link(stem: str, files: list[Path]) -> str:
    stem_l = stem.lower()
    for file in files:
        if file.stem.lower() == stem_l:
            return str(file)
    return "NEED_AUDIT_LINK"


def main() -> int:
    args = parse_args()
    tables = candidates(args.tables_dir, TABLE_EXTENSIONS)
    logs = candidates(args.logs_dir, {".log"}) if args.logs_dir else []
    do_files = candidates(args.do_dir, {".do"}) if args.do_dir else []
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=[
                "table_path",
                "format",
                "modified_time",
                "linked_spec_id",
                "linked_log",
                "linked_do_file",
                "audit_status",
            ],
        )
        writer.writeheader()
        for table in sorted(tables):
            writer.writerow(
                {
                    "table_path": str(table),
                    "format": table.suffix.lower().lstrip("."),
                    "modified_time": datetime.fromtimestamp(table.stat().st_mtime).isoformat(timespec="seconds"),
                    "linked_spec_id": "NEED_AUDIT_LINK",
                    "linked_log": infer_link(table.stem, logs),
                    "linked_do_file": infer_link(table.stem, do_files),
                    "audit_status": "NEED_AUDIT",
                }
            )
    print(f"Wrote inventory for {len(tables)} table files to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
