"""Dry-run first wrapper for executing Stata do files with safe Windows paths."""

from __future__ import annotations

import argparse
import os
import platform
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Safe wrapper for Stata execution; defaults to dry-run.")
    parser.add_argument("--stata-path", type=Path, help="Path to Stata executable. Or set STATA_PATH.")
    parser.add_argument("--do-file", required=True, type=Path)
    parser.add_argument("--log-file", required=True, type=Path)
    parser.add_argument("--project-root", required=True, type=Path)
    parser.add_argument("--command-log", type=Path, help="Write command preview and return codes to this file.")
    parser.add_argument("--expected-output", action="append", default=[], type=Path, help="Expected table/output path. Repeat for multiple outputs.")
    parser.add_argument("--timeout-seconds", type=int, default=None, help="Optional process timeout in seconds.")
    parser.add_argument("--execute", action="store_true", help="Actually run Stata.")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Preview command. Default behavior.")
    return parser.parse_args()


def quote_cmd(value: str) -> str:
    escaped = value.replace('"', r'\"')
    return f'"{escaped}"'


def relative_do_path(do_file: Path, project_root: Path) -> str:
    try:
        return str(do_file.resolve().relative_to(project_root.resolve()))
    except ValueError:
        return str(do_file)


def build_command(stata_path: Path, do_file: Path, project_root: Path) -> tuple[list[str] | str, str, bool]:
    if platform.system().lower().startswith("win"):
        rel_do = relative_do_path(do_file, project_root)
        preview = f'cmd.exe /c cd /d {quote_cmd(str(project_root))} && {quote_cmd(str(stata_path))} /e do {quote_cmd(rel_do)}'
        return preview, preview, True
    command = [str(stata_path), "/e", "do", str(do_file)]
    preview = " ".join(quote_cmd(part) if " " in part else part for part in command)
    return command, preview, False


def append_command_log(path: Path | None, text: str) -> None:
    if not path:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(text.rstrip() + "\n")


def build_status_record(
    *,
    process_returncode: int | None,
    process_timed_out: bool,
    log_file_exists: bool,
    log_parse_returncode: int | None,
    expected_outputs: list[Path],
) -> dict[str, str]:
    if process_timed_out:
        process_status = "timeout"
    elif process_returncode == 0:
        process_status = "passed"
    elif process_returncode is None:
        process_status = "not_run"
    else:
        process_status = "failed"

    if not log_file_exists:
        log_status = "missing"
        stata_error_status = "not_checked"
    elif log_parse_returncode == 0:
        log_status = "complete_success"
        stata_error_status = "passed"
    elif log_parse_returncode is None:
        log_status = "present_not_parsed"
        stata_error_status = "not_checked"
    else:
        log_status = "complete_failed"
        stata_error_status = "failed"

    if expected_outputs:
        missing_outputs = [str(path) for path in expected_outputs if not path.exists()]
        table_export_status = "failed" if missing_outputs else "passed"
    else:
        missing_outputs = []
        table_export_status = "not_applicable"

    if stata_error_status == "failed" or table_export_status == "failed" or process_status == "failed":
        run_status = "failed"
    elif process_status == "timeout" and log_status == "complete_success" and table_export_status in {"passed", "not_applicable"}:
        run_status = "completed_with_runner_warning"
    elif process_status == "passed" and log_status in {"complete_success", "present_not_parsed"} and table_export_status in {"passed", "not_applicable"}:
        run_status = "completed"
    else:
        run_status = "blocked"

    status = {
        "run_status": run_status,
        "process_status": process_status,
        "log_status": log_status,
        "stata_error_status": stata_error_status,
        "table_export_status": table_export_status,
    }
    if run_status == "completed_with_runner_warning":
        status["runner_warning"] = "Process timed out after Stata continued in batch mode; latest complete log passed."
    if missing_outputs:
        status["missing_outputs"] = "; ".join(missing_outputs)
    return status


def format_status_lines(status: dict[str, str]) -> list[str]:
    ordered_keys = [
        "run_status",
        "process_status",
        "log_status",
        "stata_error_status",
        "table_export_status",
        "runner_warning",
        "missing_outputs",
    ]
    return [f"- {key}: `{status[key]}`" for key in ordered_keys if key in status]


def main() -> int:
    args = parse_args()
    stata_path = args.stata_path or (Path(os.environ["STATA_PATH"]) if os.environ.get("STATA_PATH") else None)
    if not stata_path:
        print("P0: --stata-path or STATA_PATH is required.", file=sys.stderr)
        return 2
    if not args.do_file.exists():
        print(f"P0: do-file does not exist: {args.do_file}", file=sys.stderr)
        return 2
    if not args.project_root.exists():
        print(f"P0: project root does not exist: {args.project_root}", file=sys.stderr)
        return 2

    command, preview, use_shell = build_command(stata_path, args.do_file, args.project_root)
    command_log_header = [
        "# Stata Runner Command Log",
        "",
        f"- Generated: {datetime.now().isoformat(timespec='seconds')}",
        f"- Project root: `{args.project_root}`",
        f"- Do file: `{args.do_file}`",
        f"- Expected log file: `{args.log_file}`",
        f"- Command preview: `{preview}`",
        "",
    ]
    append_command_log(args.command_log, "\n".join(command_log_header))
    print("Command to run:")
    print(preview)
    print(f"Expected log file: {args.log_file}")
    if not args.execute:
        print("DRY RUN: Stata was not executed. Pass --execute to run after HITL approval.")
        return 0

    process_timed_out = False
    process_returncode: int | None
    try:
        result = subprocess.run(command, cwd=args.project_root, check=False, shell=use_shell, timeout=args.timeout_seconds)
        process_returncode = result.returncode
    except subprocess.TimeoutExpired:
        process_timed_out = True
        process_returncode = None

    append_command_log(args.command_log, f"- Return code: `{process_returncode if process_returncode is not None else 'timeout'}`")
    print(f"Stata return code: {process_returncode if process_returncode is not None else 'timeout'}")
    parser_path = Path(__file__).with_name("stata_log_parser.py")
    parse_returncode: int | None = None
    if args.log_file.exists() and parser_path.exists():
        parse_result = subprocess.run(
            [sys.executable, str(parser_path), "--log-file", str(args.log_file), "--fail-on-error"],
            check=False,
        )
        parse_returncode = parse_result.returncode
    elif not args.log_file.exists():
        print("Log parser was not run because the expected Stata log is missing.")
    else:
        print("Log parser was not run. Inspect the Stata log before making any result claim.")

    status = build_status_record(
        process_returncode=process_returncode,
        process_timed_out=process_timed_out,
        log_file_exists=args.log_file.exists(),
        log_parse_returncode=parse_returncode,
        expected_outputs=args.expected_output,
    )
    status_text = "\n".join(["", "## Status Record", *format_status_lines(status)])
    append_command_log(args.command_log, status_text)
    print(status_text)
    return 0 if status["run_status"] in {"completed", "completed_with_runner_warning"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
