"""Parse Stata logs for execution signals; no log means no empirical claim."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path


ACTUAL_ERROR_PATTERNS = [
    re.compile(r"^\s*r\([0-9]+\);", re.IGNORECASE),
    re.compile(r"^\s*(?:file|variable|matrix|program|command)\b.*\bnot found\b", re.IGNORECASE),
    re.compile(r"^\s*no observations\b", re.IGNORECASE),
    re.compile(r"^\s*insufficient observations\b", re.IGNORECASE),
    re.compile(r"^\s*conformability error\b", re.IGNORECASE),
    re.compile(r"^\s*no standard errors?\b", re.IGNORECASE),
]

WARNING_PATTERNS = [
    re.compile(r"\bomitted because of collinearity\b", re.IGNORECASE),
    re.compile(r"\bnote:\b.*\bomitted\b", re.IGNORECASE),
    re.compile(r"\bcollinearity\b", re.IGNORECASE),
    re.compile(r"\bmissing standard errors\b", re.IGNORECASE),
]

COMMAND_ECHO_PATTERNS = [
    re.compile(r"^\s*\.\s+"),
    re.compile(r"^\s*>\s+"),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract Stata log execution signals and context.")
    parser.add_argument("--log-file", required=True, type=Path)
    parser.add_argument("--output", type=Path, help="Markdown output path. Defaults to stdout.")
    parser.add_argument("--json-output", type=Path, help="Optional JSON output path with structured parser classifications.")
    parser.add_argument("--context-lines", type=int, default=3)
    parser.add_argument("--fail-on-error", action="store_true")
    return parser.parse_args()


def is_command_echo(line: str) -> bool:
    return any(pattern.search(line) for pattern in COMMAND_ECHO_PATTERNS)


def classify_line(line: str) -> tuple[str | None, str, float]:
    stripped = line.strip()
    if not stripped:
        return None, "none", 0.0
    if is_command_echo(line):
        echoed = stripped[1:].lstrip() if stripped[:1] in {".", ">"} else stripped
        if "display as error" in echoed.lower():
            return "command_echo", "display_as_error_echo", 0.95
        if any(pattern.search(echoed) for pattern in ACTUAL_ERROR_PATTERNS):
            return "command_echo", "echoed_error_like_code", 0.75
        if "error" in echoed.lower():
            return "command_echo", "echoed_error_text", 0.65
    if any(pattern.search(line) for pattern in ACTUAL_ERROR_PATTERNS):
        return "actual_error", "hard_error_pattern", 0.95
    if any(pattern.search(line) for pattern in WARNING_PATTERNS):
        return "warning", "model_warning_pattern", 0.85
    if "error" in stripped.lower():
        return "needs_human_review", "ambiguous_error_text", 0.5
    return None, "none", 0.0


def find_signals(lines: list[str], context: int) -> list[dict[str, object]]:
    signals: list[dict[str, object]] = []
    for index, line in enumerate(lines):
        classification, reason, confidence = classify_line(line)
        if classification:
            start = max(0, index - context)
            end = min(len(lines), index + context + 1)
            signals.append(
                {
                    "line_no": index + 1,
                    "signal": line.rstrip(),
                    "classification": classification,
                    "reason": reason,
                    "confidence": confidence,
                    "context": [item.rstrip() for item in lines[start:end]],
                }
            )
    return signals


def build_report(log_file: Path, signals: list[dict[str, object]]) -> str:
    actual_errors = [item for item in signals if item["classification"] == "actual_error"]
    review_items = [item for item in signals if item["classification"] == "needs_human_review"]
    warnings = [item for item in signals if item["classification"] == "warning"]
    lines = [
        "# Stata Log Parse Report",
        "",
        f"- Generated: {datetime.now().isoformat(timespec='seconds')}",
        f"- Log file: `{log_file}`",
        "- Scope: execution-signal parsing only; no regression results are interpreted.",
        f"- Parser confidence summary: actual_errors={len(actual_errors)}, needs_human_review={len(review_items)}, warnings={len(warnings)}",
        "",
    ]
    if not signals:
        lines += ["## Status", "", "No configured execution signals were detected. This is not a full audit pass.", ""]
        return "\n".join(lines)
    lines += ["## Execution Signals", ""]
    for item in signals:
        lines += [
            f"### Line {item['line_no']}",
            "",
            f"- Classification: `{item['classification']}`",
            f"- Reason: `{item['reason']}`",
            f"- Parser confidence: `{item['confidence']}`",
            f"- Signal: `{item['signal']}`",
            "",
            "```text",
        ]
        lines.extend(item["context"])  # type: ignore[arg-type]
        lines += ["```", ""]
    lines += ["## failed_regressions.md Input", ""]
    if actual_errors:
        for item in actual_errors:
            lines.append(f"- log_line: {item['line_no']}; failure_signal: {item['signal']}; status: P0_UNRESOLVED")
    else:
        lines.append("- No automatic P0 failure rows. Review warning and needs_human_review items before making evidence claims.")
    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    if not args.log_file.exists():
        print(f"P0: no log file found; no log, no claim: {args.log_file}", file=sys.stderr)
        return 2
    lines = args.log_file.read_text(encoding="utf-8", errors="replace").splitlines()
    signals = find_signals(lines, max(args.context_lines, 0))
    report = build_report(args.log_file, signals)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report, encoding="utf-8")
    else:
        print(report)
    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(json.dumps({"log_file": str(args.log_file), "signals": signals}, indent=2), encoding="utf-8")
    has_actual_error = any(item["classification"] == "actual_error" for item in signals)
    return 1 if has_actual_error and args.fail_on_error else 0


if __name__ == "__main__":
    raise SystemExit(main())
