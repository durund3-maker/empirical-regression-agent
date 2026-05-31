"""Build a generic evidence map from inventories and audit reports."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


EVIDENCE_CLASSES = {
    "verified_evidence",
    "author_decision",
    "agent_inference",
    "open_risk",
    "unverified_claim",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create evidence_map.csv without drafting manuscript claims.")
    parser.add_argument("--table-inventory", required=True, type=Path)
    parser.add_argument("--run-report", required=True, type=Path)
    parser.add_argument("--failed-regressions", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    return parser.parse_args()


def exists_class(path: Path, verified_if_present: bool = False) -> str:
    if not path.exists():
        return "open_risk"
    return "verified_evidence" if verified_if_present else "unverified_claim"


def main() -> int:
    args = parse_args()
    rows: list[dict[str, str]] = []
    if args.table_inventory.exists():
        with args.table_inventory.open("r", newline="", encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                audit_status = row.get("audit_status", "")
                evidence_class = "verified_evidence" if audit_status.upper() in {"PASSED", "AUDIT_PASSED"} else "unverified_claim"
                rows.append(
                    {
                        "artifact_type": "table",
                        "artifact_path": row.get("table_path", ""),
                        "evidence_class": evidence_class,
                        "source": str(args.table_inventory),
                        "notes": "Inventory row only; table numbers were not read or interpreted.",
                    }
                )
    else:
        rows.append(
            {
                "artifact_type": "table_inventory",
                "artifact_path": str(args.table_inventory),
                "evidence_class": "open_risk",
                "source": "missing input",
                "notes": "Missing table inventory.",
            }
        )

    for label, path in [("regression_run_report", args.run_report), ("failed_regressions", args.failed_regressions)]:
        rows.append(
            {
                "artifact_type": label,
                "artifact_path": str(path),
                "evidence_class": exists_class(path),
                "source": str(path) if path.exists() else "missing input",
                "notes": "Presence is mapped for audit traceability; content still requires review.",
            }
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["artifact_type", "artifact_path", "evidence_class", "source", "notes"])
        writer.writeheader()
        for row in rows:
            if row["evidence_class"] not in EVIDENCE_CLASSES:
                row["evidence_class"] = "unverified_claim"
            writer.writerow(row)
    print(f"Wrote evidence map with {len(rows)} rows to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
