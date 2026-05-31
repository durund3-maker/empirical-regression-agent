"""Check text artifacts for UTF-8 readability and common mojibake."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path


DEFAULT_SUFFIXES = {".md", ".csv", ".yml", ".yaml", ".txt", ".tex", ".do", ".py"}
MOJIBAKE_PATTERNS = [
    re.compile(r"�"),
    re.compile(r"\?{3,}"),
    re.compile(r"(?:鍒|濆||鍖|栧|苟|鍚|姩|涓|鏂|鎴|鍙|鐢|瑙|鏁|据){2,}"),
    re.compile(r"鈥|鈮|鉁|鉂|銆|乮|乫|乺"),
]


@dataclass
class EncodingFinding:
    path: str
    line: int
    reason: str
    sample: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit UTF-8 text artifacts before handoff.")
    parser.add_argument("--root", type=Path, help="Root directory to scan.")
    parser.add_argument("--path", action="append", type=Path, default=[], help="Specific file to scan. Repeatable.")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json-output", type=Path)
    parser.add_argument("--fail-on-finding", action="store_true")
    return parser.parse_args()


def iter_files(root: Path | None, paths: list[Path]) -> list[Path]:
    files = [path for path in paths if path.exists() and path.is_file()]
    if root and root.exists():
        files.extend(path for path in root.rglob("*") if path.is_file() and path.suffix.lower() in DEFAULT_SUFFIXES)
    return sorted(set(files))


def check_file(path: Path) -> list[EncodingFinding]:
    try:
        text = path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError as exc:
        return [EncodingFinding(str(path), 0, f"not valid UTF-8: {exc}", "")]
    findings: list[EncodingFinding] = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        for pattern in MOJIBAKE_PATTERNS:
            if pattern.search(line):
                findings.append(EncodingFinding(str(path), line_no, f"mojibake pattern `{pattern.pattern}`", line.strip()[:160]))
                break
    return findings


def build_report(files: list[Path], findings: list[EncodingFinding]) -> str:
    lines = [
        "# Encoding Audit Report",
        "",
        f"- Generated: {datetime.now().isoformat(timespec='seconds')}",
        f"- Files scanned: {len(files)}",
        f"- Status: `{'BLOCKED' if findings else 'PASS'}`",
        "- Policy: Markdown/YAML/TXT/Python/Stata text must be UTF-8; final Excel-facing CSV may use UTF-8-SIG when documented.",
        "",
    ]
    if not findings:
        lines.append("No UTF-8 decode failures or configured mojibake patterns were detected.")
        return "\n".join(lines) + "\n"
    lines += ["## Findings", ""]
    for finding in findings:
        lines.append(f"- `{finding.path}:{finding.line}` {finding.reason}: `{finding.sample}`")
    lines += ["", "Mojibake findings block final handoff until corrected or explicitly excluded from the package."]
    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    files = iter_files(args.root, args.path)
    if not files:
        print("No files to scan.", file=sys.stderr)
        return 2
    findings: list[EncodingFinding] = []
    for path in files:
        findings.extend(check_file(path))
    report = build_report(files, findings)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report, encoding="utf-8")
    else:
        print(report)
    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(json.dumps([asdict(item) for item in findings], indent=2), encoding="utf-8")
    return 1 if findings and args.fail_on_finding else 0


if __name__ == "__main__":
    raise SystemExit(main())
