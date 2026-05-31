"""Report Git-tracked data and archive risks without deleting or editing files."""

from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime
from pathlib import Path


RISK_EXTENSIONS = {".dta", ".parquet", ".csv", ".xlsx", ".xls", ".zip", ".rar", ".7z", ".log"}
RAW_SEGMENTS = {"raw", "raw_data", "original", "source_data"}
PROCESSED_SEGMENTS = {"processed", "derived", "cleaned", "intermediate"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit risky data files tracked by Git or present in a project.")
    parser.add_argument("--project-root", required=True, type=Path)
    parser.add_argument("--output", type=Path, help="Markdown output path. Defaults to stdout.")
    parser.add_argument("--max-size-mb", type=float, default=50.0)
    parser.add_argument("--fail-on-risk", action="store_true")
    return parser.parse_args()


def git_tracked(root: Path) -> set[Path]:
    try:
        result = subprocess.run(
            ["git", "ls-files"],
            cwd=root,
            text=True,
            capture_output=True,
            check=False,
        )
    except OSError:
        return set()
    if result.returncode != 0:
        return set()
    return {root / line.strip() for line in result.stdout.splitlines() if line.strip()}


def iter_files(root: Path) -> list[Path]:
    ignored_dirs = {".git", "__pycache__", ".pytest_cache"}
    files: list[Path] = []
    for path in root.rglob("*"):
        if any(part in ignored_dirs for part in path.parts):
            continue
        if path.is_file():
            files.append(path)
    return files


def classify(path: Path, root: Path, tracked: set[Path], max_size: int) -> list[str]:
    reasons: list[str] = []
    rel_parts = {part.lower() for part in path.relative_to(root).parts}
    suffix = path.suffix.lower()
    if path in tracked and suffix in RISK_EXTENSIONS:
        reasons.append("Git tracks a data/log/archive extension")
    if path in tracked and rel_parts & RAW_SEGMENTS:
        reasons.append("Git tracks a file under a raw/source data path")
    if path in tracked and rel_parts & PROCESSED_SEGMENTS:
        reasons.append("Git tracks a file under a processed/derived data path")
    try:
        size = path.stat().st_size
    except OSError:
        size = 0
    if size > max_size:
        reasons.append(f"Large file exceeds {max_size / 1024 / 1024:.1f} MB")
    if suffix in {".zip", ".rar", ".7z"}:
        reasons.append("Archive file requires explicit confidentiality review")
    return reasons


def build_report(root: Path, risks: list[tuple[Path, list[str]]]) -> str:
    lines = [
        "# Data Safety Risks",
        "",
        f"- Generated: {datetime.now().isoformat(timespec='seconds')}",
        f"- Project root: `{root}`",
        "- Scope: report only; no files were deleted or modified.",
        "",
    ]
    if not risks:
        lines += ["## Status", "", "No tracked data safety risks were detected by this script.", ""]
        return "\n".join(lines)
    lines += ["## Risks", ""]
    for path, reasons in risks:
        lines.append(f"- `{path.relative_to(root)}`")
        for reason in reasons:
            lines.append(f"  - {reason}")
    lines += ["", "## Required Handling", "", "Review AGENTS.md and project confidentiality metadata before any Git changes."]
    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    root = args.project_root.resolve()
    if not root.exists():
        print(f"P0: project root does not exist: {root}", file=sys.stderr)
        return 2
    tracked = git_tracked(root)
    max_size = int(args.max_size_mb * 1024 * 1024)
    risks = [(p, r) for p in iter_files(root) if (r := classify(p, root, tracked, max_size))]
    report = build_report(root, risks)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report, encoding="utf-8")
    else:
        print(report)
    return 1 if risks and args.fail_on_risk else 0


if __name__ == "__main__":
    raise SystemExit(main())
