"""Validate generic regression_specs.yml records without running regressions."""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


FIELD_ALIASES = {
    "outcome": ["outcome", "dependent_variable"],
    "treatment": ["treatment", "treatment_or_key_variable", "key_variable"],
    "controls": ["controls"],
    "fixed_effects": ["fixed_effects"],
    "cluster": ["cluster", "clustering"],
    "sample_condition": ["sample_condition", "sample_filter"],
    "estimator": ["estimator"],
    "expected_table": ["expected_table"],
    "expected_log": ["expected_log"],
    "human_confirmed": ["human_confirmed"],
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check regression specs for required fields and HITL approval.")
    parser.add_argument("--spec-file", required=True, type=Path)
    parser.add_argument("--schema-file", type=Path, help="Optional schema path recorded for traceability.")
    parser.add_argument("--output", type=Path, help="Markdown validation report. Defaults to stdout.")
    parser.add_argument("--fail-on-p0", action="store_true")
    return parser.parse_args()


def load_yaml(path: Path) -> Any:
    try:
        import yaml  # type: ignore
    except ImportError as exc:
        raise RuntimeError("PyYAML is required to read YAML specs. Install pyyaml or export specs as JSON.") from exc
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def as_records(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, list):
        return [r for r in data if isinstance(r, dict)]
    if isinstance(data, dict):
        for key in ("regression_specs", "specs", "models"):
            if isinstance(data.get(key), list):
                return [r for r in data[key] if isinstance(r, dict)]
        if any(alias in data for aliases in FIELD_ALIASES.values() for alias in aliases):
            return [data]
    return []


def field_value(record: dict[str, Any], canonical: str) -> Any:
    if canonical == "expected_table":
        outputs = record.get("expected_outputs")
        if isinstance(outputs, list):
            return next((x for x in outputs if str(x).lower().endswith((".rtf", ".tex", ".csv", ".xlsx"))), None)
    if canonical == "expected_log":
        outputs = record.get("expected_outputs")
        if isinstance(outputs, list):
            return next((x for x in outputs if str(x).lower().endswith(".log")), None)
    if canonical == "human_confirmed" and "approval_status" in record:
        return str(record.get("approval_status")).lower() == "approved"
    for alias in FIELD_ALIASES[canonical]:
        if alias in record:
            return record[alias]
    return None


def is_missing(value: Any) -> bool:
    return value is None or value == "" or value == "NEED_AUTHOR_CONFIRMATION"


def confirmed(record: dict[str, Any]) -> bool:
    value = field_value(record, "human_confirmed")
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"yes", "true", "1", "approved", "confirmed"}


def main() -> int:
    args = parse_args()
    if not args.spec_file.exists():
        print(f"P0: spec file does not exist: {args.spec_file}", file=sys.stderr)
        return 2
    try:
        records = as_records(load_yaml(args.spec_file))
    except Exception as exc:
        print(f"P0: could not load specs: {exc}", file=sys.stderr)
        return 2

    p0: list[str] = []
    lines = [
        "# Regression Spec Validation",
        "",
        f"- Generated: {datetime.now().isoformat(timespec='seconds')}",
        f"- Spec file: `{args.spec_file}`",
        f"- Schema file: `{args.schema_file}`" if args.schema_file else "- Schema file: not provided",
        "- Scope: validation only; no regressions were run and specs were not modified.",
        "",
    ]
    if not records:
        p0.append("No regression spec records found.")
    for idx, record in enumerate(records, start=1):
        spec_id = record.get("spec_id", f"record_{idx}")
        missing = [name for name in FIELD_ALIASES if is_missing(field_value(record, name))]
        if missing:
            p0.append(f"{spec_id}: missing required fields: {', '.join(missing)}")
        if not confirmed(record):
            p0.append(f"{spec_id}: human_confirmed is not true or approval_status is not approved")

    lines += ["## P0 Findings", ""]
    lines += [f"- {item}" for item in p0] if p0 else ["No P0 findings detected by this validator."]
    report = "\n".join(lines) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report, encoding="utf-8")
    else:
        print(report)
    return 1 if p0 and args.fail_on_p0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
