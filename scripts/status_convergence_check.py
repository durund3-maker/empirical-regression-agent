"""Check final handoff status records for contradictions before completion."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path


COMPLETE_PATTERNS = [re.compile(r"\bcomplete(?:d)?\b", re.IGNORECASE), re.compile(r"\bprepared\b", re.IGNORECASE)]
INCOMPLETE_PATTERNS = [
    re.compile(r"\bpending\b", re.IGNORECASE),
    re.compile(r"\bnot[_ -]?approved\b", re.IGNORECASE),
    re.compile(r"\bnot[_ -]?executed\b", re.IGNORECASE),
    re.compile(r"\bproposal[_ -]?only\b", re.IGNORECASE),
    re.compile(r"\bremains to be built\b", re.IGNORECASE),
    re.compile(r"\bTODO\b", re.IGNORECASE),
]
OPEN_P0_PATTERN = re.compile(r"\bP0\b.{0,40}\b(open|unresolved|blocked)\b", re.IGNORECASE)


@dataclass
class Finding:
    path: str
    severity: str
    message: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Block handoff completion when status files conflict.")
    parser.add_argument("--project-root", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json-output", type=Path)
    parser.add_argument("--fail-on-conflict", action="store_true")
    return parser.parse_args()


def iter_status_files(project_root: Path) -> list[Path]:
    candidates: list[Path] = []
    for folder in ["review", "handoff_package"]:
        root = project_root / folder
        if root.exists():
            candidates.extend(path for path in root.rglob("*") if path.suffix.lower() in {".md", ".csv", ".yml", ".yaml", ".txt"})
    return candidates


def check_text_file(path: Path) -> list[Finding]:
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    findings: list[Finding] = []
    has_complete = any(pattern.search(text) for pattern in COMPLETE_PATTERNS)
    has_incomplete = any(pattern.search(text) for pattern in INCOMPLETE_PATTERNS)
    if has_complete and has_incomplete:
        findings.append(Finding(str(path), "P0", "Conflicting complete and incomplete/pending/TODO language in the same status artifact."))
    if OPEN_P0_PATTERN.search(text):
        findings.append(Finding(str(path), "P0", "Open or unresolved P0 language remains before handoff completion."))
    if "empirical-paper-agent" in text and re.search(r"\btransfer\b", text, re.IGNORECASE) and re.search(r"\bnot[_ -]?approved\b", text, re.IGNORECASE):
        findings.append(Finding(str(path), "P0", "Transfer status is not approved; package must not be transferred."))
    return findings


def check_handoff_manifest(project_root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for manifest in [project_root / "handoff_package" / "file_manifest.csv", project_root / "handoff_package" / "evidence_map.csv"]:
        if not manifest.exists():
            continue
        with manifest.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            for idx, row in enumerate(reader, start=2):
                joined = " ".join(str(value) for value in row.values()).lower()
                if any(token in joined for token in ["pending", "proposal", "not_executed", "unverified", "not approved"]):
                    findings.append(Finding(str(manifest), "P0", f"Row {idx} includes pending/proposal/not_executed/unverified material in handoff manifest."))
    return findings


def build_report(project_root: Path, findings: list[Finding]) -> str:
    lines = [
        "# Status Convergence Report",
        "",
        f"- Generated: {datetime.now().isoformat(timespec='seconds')}",
        f"- Project root: `{project_root}`",
        f"- Status: `{'BLOCKED' if findings else 'PASS'}`",
        "",
    ]
    if not findings:
        lines.append("No status convergence conflicts were detected. This does not replace a full empirical audit.")
        return "\n".join(lines) + "\n"
    lines += ["## Blocking Findings", ""]
    for finding in findings:
        lines.append(f"- `{finding.severity}` `{finding.path}`: {finding.message}")
    lines += ["", "## Required Action", "", "Resolve status conflicts before marking handoff complete or transferring to empirical-paper-agent."]
    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    if not args.project_root.exists():
        print(f"Project root not found: {args.project_root}", file=sys.stderr)
        return 2
    findings: list[Finding] = []
    for path in iter_status_files(args.project_root):
        findings.extend(check_text_file(path))
    findings.extend(check_handoff_manifest(args.project_root))
    report = build_report(args.project_root, findings)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report, encoding="utf-8")
    else:
        print(report)
    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(json.dumps([asdict(item) for item in findings], indent=2), encoding="utf-8")
    return 1 if findings and args.fail_on_conflict else 0


if __name__ == "__main__":
    raise SystemExit(main())
