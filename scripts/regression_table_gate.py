"""Hard gate regression tables before bundle or handoff inclusion."""

from __future__ import annotations

import argparse
import csv
import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path


SE_MISSING_VALUES = {"(.)", ".", "", "nan", "na", "n/a"}
SERIOUS_LOG_PATTERNS = [
    re.compile(r"omitted because of collinearity", re.IGNORECASE),
    re.compile(r"\bnote:\b.*\bomitted\b", re.IGNORECASE),
    re.compile(r"no standard errors?", re.IGNORECASE),
    re.compile(r"insufficient observations", re.IGNORECASE),
    re.compile(r"no observations", re.IGNORECASE),
    re.compile(r"not estimable", re.IGNORECASE),
]


@dataclass
class GateResult:
    table: str
    status: str
    reasons: list[str]
    n_min: int | None = None
    r2_max: float | None = None
    se_all_missing: bool = False
    estimated_parameters: int | None = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Reject pathological regression tables from main bundles.")
    parser.add_argument("--table", action="append", type=Path, required=True, help="CSV/TEX/RTF table path. Repeatable.")
    parser.add_argument("--log-file", action="append", type=Path, default=[], help="Optional linked Stata log path. Repeatable.")
    parser.add_argument("--output", type=Path, help="Markdown audit output.")
    parser.add_argument("--json-output", type=Path, help="Structured JSON output.")
    parser.add_argument("--min-n", type=int, default=30)
    parser.add_argument("--r2-near-one-threshold", type=float, default=0.995)
    parser.add_argument("--min-obs-per-parameter", type=float, default=5.0)
    parser.add_argument("--baseline-n", type=int, help="Original or intended analysis sample size.")
    parser.add_argument("--max-unexplained-sample-loss", type=float, default=0.5)
    parser.add_argument("--fail-on-hard-gate", action="store_true")
    return parser.parse_args()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def numeric_from_cell(value: str) -> float | None:
    cleaned = value.strip().replace(",", "").replace("$", "").replace("\\", "")
    match = re.search(r"-?\d+(?:\.\d+)?", cleaned)
    return float(match.group(0)) if match else None


def table_rows(path: Path) -> list[list[str]]:
    if path.suffix.lower() != ".csv":
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [row for row in csv.reader(handle)]


def extract_n_values(text: str, rows: list[list[str]]) -> list[int]:
    values: list[int] = []
    for row in rows:
        if row and re.search(r"^(n|obs|observations|sample size)$", row[0].strip(), re.IGNORECASE):
            for cell in row[1:]:
                number = numeric_from_cell(cell)
                if number is not None:
                    values.append(int(number))
    for match in re.finditer(r"\b(?:N|Observations|Obs\.?)\b[^0-9]{0,20}([0-9][0-9,]*)", text, re.IGNORECASE):
        values.append(int(match.group(1).replace(",", "")))
    return values


def extract_r2_values(text: str, rows: list[list[str]]) -> list[float]:
    values: list[float] = []
    for row in rows:
        if row and re.search(r"r-?sq|r\^2|r2", row[0].strip(), re.IGNORECASE):
            for cell in row[1:]:
                number = numeric_from_cell(cell)
                if number is not None:
                    values.append(number)
    for match in re.finditer(r"(?:R-sq|R\^2|R2|R-squared)[^0-9]{0,20}([01](?:\.\d+)?)", text, re.IGNORECASE):
        values.append(float(match.group(1)))
    return values


def count_parameter_rows(rows: list[list[str]]) -> int | None:
    if not rows:
        return None
    count = 0
    statistic_labels = re.compile(r"^(n|obs|observations|r-?sq|r2|controls|fixed effects|fe|sample)$", re.IGNORECASE)
    for row in rows:
        if not row or not row[0].strip() or statistic_labels.search(row[0].strip()):
            continue
        if any(numeric_from_cell(cell) is not None or cell.strip().lower() in SE_MISSING_VALUES for cell in row[1:]):
            count += 1
    return count or None


def standard_errors_all_missing(rows: list[list[str]]) -> bool:
    se_cells: list[str] = []
    for row in rows:
        if row and (row[0].strip() == "" or re.search(r"se|std", row[0], re.IGNORECASE)):
            se_cells.extend(cell.strip().lower() for cell in row[1:] if cell.strip())
    if not se_cells:
        return False
    return all(cell in SE_MISSING_VALUES for cell in se_cells)


def audit_table(path: Path, args: argparse.Namespace, log_text: str) -> GateResult:
    if not path.exists():
        return GateResult(str(path), "BLOCK_MAIN_BUNDLE", [f"table file missing: {path}"])
    text = read_text(path)
    rows = table_rows(path)
    reasons: list[str] = []
    n_values = extract_n_values(text, rows)
    n_min = min(n_values) if n_values else None
    if n_min is not None and n_min < args.min_n:
        reasons.append(f"N below hard-gate threshold: min N={n_min}, threshold={args.min_n}")
    if n_min is not None and args.baseline_n and args.baseline_n > 0:
        loss = 1 - (n_min / args.baseline_n)
        if loss > args.max_unexplained_sample_loss:
            reasons.append(f"Actual estimation sample is too far from baseline without documented explanation: loss={loss:.3f}")
    r2_values = extract_r2_values(text, rows)
    r2_max = max(r2_values) if r2_values else None
    if r2_max is not None and r2_max >= args.r2_near_one_threshold:
        reasons.append(f"R-sq equals or is near 1 without documented explanation: max R-sq={r2_max:.3f}")
    se_missing = standard_errors_all_missing(rows)
    if se_missing:
        reasons.append("Standard errors are all missing.")
    parameter_count = count_parameter_rows(rows)
    if n_min and parameter_count and n_min / parameter_count < args.min_obs_per_parameter:
        reasons.append(f"Too many model parameters for sample size: N/parameters={n_min / parameter_count:.2f}, threshold={args.min_obs_per_parameter}")
    for pattern in SERIOUS_LOG_PATTERNS:
        if pattern.search(text) or pattern.search(log_text):
            reasons.append(f"Serious Stata/table signal detected: {pattern.pattern}")
    status = "BLOCK_MAIN_BUNDLE" if reasons else "PASS"
    return GateResult(str(path), status, reasons, n_min, r2_max, se_missing, parameter_count)


def build_report(results: list[GateResult], args: argparse.Namespace) -> str:
    lines = [
        "# Regression Table Gate Report",
        "",
        f"- Generated: {datetime.now().isoformat(timespec='seconds')}",
        f"- Thresholds: min_n={args.min_n}, r2_near_one_threshold={args.r2_near_one_threshold}, min_obs_per_parameter={args.min_obs_per_parameter}",
        "- Gate rule: tables with `BLOCK_MAIN_BUNDLE` must be excluded from manuscript-ready tables and handoff main evidence.",
        "",
    ]
    for result in results:
        lines += [
            f"## {Path(result.table).name}",
            "",
            f"- status: `{result.status}`",
            f"- n_min: `{result.n_min}`",
            f"- r2_max: `{result.r2_max}`",
            f"- se_all_missing: `{result.se_all_missing}`",
            f"- estimated_parameters: `{result.estimated_parameters}`",
            "- downgrade decision: `appendix_diagnostic_or_excluded`" if result.status != "PASS" else "- downgrade decision: `none`",
            "",
        ]
        if result.reasons:
            lines.append("### Reasons")
            lines.extend(f"- {reason}" for reason in result.reasons)
            lines.append("")
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    log_text = "\n".join(read_text(path) for path in args.log_file if path.exists())
    results = [audit_table(path, args, log_text) for path in args.table]
    report = build_report(results, args)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report, encoding="utf-8")
    else:
        print(report)
    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(json.dumps([asdict(result) for result in results], indent=2), encoding="utf-8")
    has_block = any(result.status != "PASS" for result in results)
    return 1 if has_block and args.fail_on_hard_gate else 0


if __name__ == "__main__":
    raise SystemExit(main())
