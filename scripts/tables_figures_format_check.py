"""Static format audit for Tables and Figures plus Appendix LaTeX bundles."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class FormatIssue:
    code: str
    message: str
    source: str = "tex"
    line: int | None = None
    context: str = ""


@dataclass(frozen=True)
class AuditResult:
    path: Path
    tex_path: Path
    passed: bool
    issues: list[FormatIssue]
    pdf_path: Path | None = None
    log_path: Path | None = None
    rendered_qa_path: Path | None = None
    final_mode: bool = False
    status_fields: dict[str, str] | None = None


TABLE_ENV_RE = re.compile(r"\\begin\{table\}.*?\\end\{table\}", re.DOTALL)
CAPTION_RE = re.compile(r"\\caption(?:\[[^\]]*\])?\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}", re.DOTALL)
TABLE_NUM_RE = re.compile(r"Table\s*\.?\s*(\d+)", re.IGNORECASE)
APPENDIX_RE = re.compile(r"(\\appendix|\\section\*\{Appendix\}|\{\\Large\s+\\textbf\{Appendix\}\})")
LONG_DECIMAL_RE = re.compile(r"(?<![A-Za-z])[-+]?\d+\.\d{4,}(?![A-Za-z])")
PLACEHOLDER_RE = re.compile(r"<[^>\n]+>|PLACEHOLDER|TODO|TBD", re.IGNORECASE)
MIXED_DUPLICATE_CAPTION_RE = re.compile(
    r"(?:表|图|圖|Table)\s*\.?\s*\d+\s*[:：]\s*Table\s*\.?\s*\d+",
    re.IGNORECASE,
)
LATEX_FATAL_RE = re.compile(
    r"^! |Emergency stop|Fatal error|LaTeX Error:|Undefined control sequence",
    re.IGNORECASE,
)
QA_STATUS_PRIORITY = {
    "failed": 4,
    "environment_blocker": 3,
    "pending": 2,
    "passed": 1,
    "missing": 0,
}


def _caption(table: str) -> str:
    match = CAPTION_RE.search(table)
    return match.group(1).strip() if match else ""


def _table_number(caption: str) -> int | None:
    match = TABLE_NUM_RE.search(caption)
    return int(match.group(1)) if match else None


def _is_appendix_table(caption: str) -> bool:
    return "appendix" in caption.lower()


def _has_pagebreak_before(text: str, start: int) -> bool:
    prefix = text[max(0, start - 250) : start]
    return bool(re.search(r"\\(?:clearpage|newpage)\b", prefix))


def _note_is_centered(table: str) -> bool:
    if r"\begin{threeparttable}" in table and r"\begin{tablenotes}" in table:
        return True
    if re.search(r"\\begin\{center\}.*?\\begin\{minipage\}", table, re.DOTALL):
        return True
    if re.search(r"\\begin\{minipage\}\{0\.\d+\\textwidth\}", table, re.DOTALL) and r"\centering" in table:
        return True
    return False


def _line_number(text: str, position: int) -> int:
    return text.count("\n", 0, position) + 1


def _compact_context(value: str, limit: int = 160) -> str:
    compact = re.sub(r"\s+", " ", value).strip()
    return compact[:limit]


def _booktabs_issue(table: str, caption: str, start_line: int) -> FormatIssue | None:
    required = {
        "toprule": r"\toprule",
        "midrule": r"\midrule",
        "bottomrule": r"\bottomrule",
    }
    for name, marker in required.items():
        if marker not in table:
            return FormatIssue(
                f"missing_booktabs_{name}",
                f"{caption or 'Untitled table'} lacks required booktabs marker {marker}.",
                line=start_line,
                context=_compact_context(caption or table),
            )
    return None


def _audit_log(log_path: Path) -> list[FormatIssue]:
    issues: list[FormatIssue] = []
    if not log_path.exists():
        return [
            FormatIssue(
                "latex_log_missing",
                f"Expected LaTeX log is missing: {log_path}",
                source="log",
                context=str(log_path),
            )
        ]
    for idx, line in enumerate(log_path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
        if "Float too large" in line:
            issues.append(
                FormatIssue(
                    "latex_float_too_large",
                    "LaTeX log reports a float too large for the page.",
                    source="log",
                    line=idx,
                    context=_compact_context(line),
                )
            )
        elif LATEX_FATAL_RE.search(line):
            issues.append(
                FormatIssue(
                    "latex_error",
                    "LaTeX log reports a fatal or structural compilation error.",
                    source="log",
                    line=idx,
                    context=_compact_context(line),
                )
            )
    return issues


def _normalize_qa_status(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    normalized = value.strip().lower()
    if normalized in {"pass", "passed"}:
        return "passed"
    if normalized in {"fail", "failed"}:
        return "failed"
    if normalized == "pending":
        return "pending"
    if normalized == "environment_blocker":
        return "environment_blocker"
    return None


def _highest_risk_status(statuses: set[str]) -> str:
    if not statuses:
        return "missing"
    return max(statuses, key=lambda status: QA_STATUS_PRIORITY[status])


def _json_qa_statuses(text: str) -> set[str] | None:
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        return None
    if not isinstance(parsed, dict):
        return set()
    statuses: set[str] = set()
    for key in ("pdf_rendered_qa_status", "status"):
        normalized = _normalize_qa_status(parsed.get(key))
        if normalized:
            statuses.add(normalized)
    return statuses


def _text_qa_statuses(text: str) -> set[str]:
    statuses: set[str] = set()
    patterns = [
        ("failed", r"(?im)^\s*Status\s*:\s*FAIL\s*$"),
        ("failed", r"(?im)^\s*pdf_rendered_qa_status\s*:\s*(failed|fail)\s*$"),
        ("environment_blocker", r"(?im)^\s*pdf_rendered_qa_status\s*:\s*environment_blocker\s*$"),
        ("pending", r"(?im)^\s*pdf_rendered_qa_status\s*:\s*pending\s*$"),
        ("passed", r"(?im)^\s*Status\s*:\s*PASS\s*$"),
        ("passed", r"(?im)^\s*pdf_rendered_qa_status\s*:\s*passed\s*$"),
    ]
    for status, pattern in patterns:
        if re.search(pattern, text):
            statuses.add(status)
    return statuses


def _read_rendered_qa_status(rendered_qa_path: Path | None) -> tuple[str, FormatIssue | None]:
    if rendered_qa_path is None:
        return "missing", FormatIssue(
            "pdf_rendered_qa_missing",
            "Final mode requires a rendered-page PDF QA record.",
            source="pdf_rendered_qa",
            context="not_provided",
        )
    if not rendered_qa_path.exists():
        return "missing", FormatIssue(
            "pdf_rendered_qa_missing",
            f"Rendered-page PDF QA record is missing: {rendered_qa_path}",
            source="pdf_rendered_qa",
            context=str(rendered_qa_path),
        )

    text = rendered_qa_path.read_text(encoding="utf-8", errors="replace")
    json_statuses = _json_qa_statuses(text)
    statuses = json_statuses if json_statuses is not None else _text_qa_statuses(text)
    status = _highest_risk_status(statuses)

    if status == "passed":
        return status, None
    if len(statuses) > 1:
        return status, FormatIssue(
            "pdf_rendered_qa_conflicting_status",
            "Rendered-page PDF QA record contains conflicting statuses; using the highest-risk status.",
            source="pdf_rendered_qa",
            context=_compact_context(text or str(rendered_qa_path)),
        )
    code = {
        "failed": "pdf_rendered_qa_failed",
        "pending": "pdf_rendered_qa_pending",
        "environment_blocker": "pdf_rendered_qa_environment_blocker",
        "missing": "pdf_rendered_qa_missing",
    }[status]
    return status, FormatIssue(
        code,
        "Rendered-page PDF QA status does not pass final bundle requirements.",
        source="pdf_rendered_qa",
        context=_compact_context(text or str(rendered_qa_path)),
    )


def audit_tex(
    path: Path,
    pdf_path: Path | None = None,
    log_path: Path | None = None,
    rendered_qa_path: Path | None = None,
    final_mode: bool = False,
) -> AuditResult:
    text = path.read_text(encoding="utf-8", errors="replace")
    issues: list[FormatIssue] = []
    tables = [(match.start(), match.group(0), _caption(match.group(0))) for match in TABLE_ENV_RE.finditer(text)]

    for start, table, caption in tables:
        if re.search(r"Table\s*\.?\s*\d+\s*:\s*Table\s*\.?\s*\d+", caption, re.IGNORECASE):
            issues.append(
                FormatIssue(
                    "duplicate_table_number",
                    f"Repeated table number in caption: {caption}",
                    line=_line_number(text, start),
                    context=_compact_context(caption),
                )
            )
        if MIXED_DUPLICATE_CAPTION_RE.search(caption):
            issues.append(
                FormatIssue(
                    "mixed_duplicate_table_number",
                    f"Mixed automatic/manual table numbering in caption: {caption}",
                    line=_line_number(text, start),
                    context=_compact_context(caption),
                )
            )
        booktabs_issue = _booktabs_issue(table, caption, _line_number(text, start))
        if booktabs_issue:
            issues.append(booktabs_issue)

    main_tables = [(start, table, caption) for start, table, caption in tables if not _is_appendix_table(caption)]
    for start, _, caption in main_tables:
        number = _table_number(caption)
        if number is not None and number >= 2 and not _has_pagebreak_before(text, start):
            issues.append(
                FormatIssue(
                    "missing_main_table_pagebreak",
                    f"Main {caption} lacks preceding clearpage/newpage.",
                    line=_line_number(text, start),
                    context=_compact_context(caption),
                )
            )

    appendix_match = APPENDIX_RE.search(text)
    if appendix_match:
        appendix_pos = appendix_match.start()
        last_main_start = main_tables[-1][0] if main_tables else -1
        if last_main_start > appendix_pos:
            issues.append(
                FormatIssue(
                    "appendix_before_last_main_table",
                    "Appendix marker appears before the last main table.",
                    line=_line_number(text, appendix_pos),
                    context="Appendix marker",
                )
            )
        if not _has_pagebreak_before(text, appendix_pos):
            issues.append(
                FormatIssue(
                    "appendix_missing_clearpage",
                    "Appendix marker lacks preceding clearpage/newpage.",
                    line=_line_number(text, appendix_pos),
                    context="Appendix marker",
                )
            )
        appendix_block = text[max(0, appendix_pos - 80) : appendix_pos + 180]
        if not re.search(r"\\begin\{center\}.*?Appendix.*?\\end\{center\}", appendix_block, re.DOTALL):
            issues.append(
                FormatIssue(
                    "appendix_not_centered",
                    "Appendix title is not in a centered block.",
                    line=_line_number(text, appendix_pos),
                    context="Appendix marker",
                )
            )
        appendix_tables = [
            (start, caption)
            for start, _, caption in tables
            if start > appendix_pos and _is_appendix_table(caption)
        ]
        if appendix_tables:
            first_appendix_table_start, first_appendix_caption = appendix_tables[0]
            between = text[appendix_match.end() : first_appendix_table_start]
            if re.search(r"\\(?:clearpage|newpage)\b", between):
                issues.append(
                    FormatIssue(
                        "appendix_first_table_separated",
                        "Appendix title is separated from the first appendix table by a page break.",
                        line=_line_number(text, first_appendix_table_start),
                        context=_compact_context(first_appendix_caption),
                    )
                )
    else:
        issues.append(FormatIssue("appendix_missing", "Appendix marker is missing."))

    for _, table, caption in tables:
        if re.search(r"\bNotes?:|\bNote:", table) and not _note_is_centered(table):
            issues.append(
                FormatIssue(
                    "note_not_centered",
                    f"Note for {caption or 'untitled table'} is not centered or in tablenotes.",
                    context=_compact_context(caption or table),
                )
            )

    if LONG_DECIMAL_RE.search(text):
        match = LONG_DECIMAL_RE.search(text)
        issues.append(
            FormatIssue(
                "long_decimal",
                "The bundle contains numeric values with more than three decimal places.",
                line=_line_number(text, match.start()) if match else None,
                context=_compact_context(match.group(0) if match else ""),
            )
        )

    if PLACEHOLDER_RE.search(text):
        match = PLACEHOLDER_RE.search(text)
        issues.append(
            FormatIssue(
                "placeholder",
                "The bundle contains unresolved placeholder text.",
                line=_line_number(text, match.start()) if match else None,
                context=_compact_context(match.group(0) if match else ""),
            )
        )

    if pdf_path is None:
        pdf_existence_status = "not_provided"
        if final_mode:
            issues.append(
                FormatIssue(
                    "pdf_missing",
                    "Final mode requires a compiled PDF path.",
                    source="pdf",
                    context="not_provided",
                )
            )
    elif not pdf_path.exists():
        pdf_existence_status = "missing"
        issues.append(FormatIssue("pdf_missing", f"Expected compiled PDF is missing: {pdf_path}", source="pdf", context=str(pdf_path)))
    else:
        pdf_existence_status = "passed"

    if log_path is None:
        latex_log_status = "not_provided"
        if final_mode:
            issues.append(
                FormatIssue(
                    "latex_log_missing",
                    "Final mode requires a LaTeX log path.",
                    source="log",
                    context="not_provided",
                )
            )
    else:
        log_issues = _audit_log(log_path)
        issues.extend(log_issues)
        latex_log_status = "failed" if log_issues else "passed"

    if final_mode:
        rendered_qa_status, rendered_qa_issue = _read_rendered_qa_status(rendered_qa_path)
        if rendered_qa_issue:
            issues.append(rendered_qa_issue)
    else:
        rendered_qa_status = "not_required"

    static_issue_sources = {issue.source for issue in issues if issue.source == "tex"}
    status_fields = {
        "static_tex_audit_status": "failed" if static_issue_sources else "passed",
        "latex_log_audit_status": latex_log_status,
        "pdf_existence_status": pdf_existence_status,
        "pdf_rendered_qa_status": rendered_qa_status,
    }

    return AuditResult(
        path=path,
        tex_path=path,
        passed=not issues,
        issues=issues,
        pdf_path=pdf_path,
        log_path=log_path,
        rendered_qa_path=rendered_qa_path,
        final_mode=final_mode,
        status_fields=status_fields,
    )


def write_report(result: AuditResult, report_path: Path) -> None:
    lines = [
        "# Tables/Figures Format Audit",
        "",
        f"- Source: `{result.tex_path.as_posix()}`",
        f"- PDF: `{result.pdf_path.as_posix() if result.pdf_path else 'not_provided'}`",
        f"- LaTeX log: `{result.log_path.as_posix() if result.log_path else 'not_provided'}`",
        f"- PDF rendered QA: `{result.rendered_qa_path.as_posix() if result.rendered_qa_path else 'not_provided'}`",
        f"- Final mode: `{result.final_mode}`",
        f"- Status: `{'PASS' if result.passed else 'FAIL'}`",
        "",
        "## Status Fields",
    ]
    for key, value in (result.status_fields or {}).items():
        lines.append(f"- {key}: `{value}`")
    lines.extend([
        "",
        "## Issues",
    ])
    if result.issues:
        for issue in result.issues:
            location = f" line {issue.line}" if issue.line is not None else ""
            lines.append(f"- `{issue.code}`: {issue.message}")
            lines.append(f"  Source: {issue.source}{location}")
            lines.append(f"  Context: `{issue.context or 'not_available'}`")
    else:
        lines.append("- No issues found after checking TeX structure, optional LaTeX log, and optional PDF path.")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit a Tables and Figures plus Appendix .tex bundle.")
    parser.add_argument("tex_path", type=Path)
    parser.add_argument("--report", type=Path, default=None)
    parser.add_argument("--pdf-path", type=Path, default=None, help="Optional compiled PDF path to require for post-build audit.")
    parser.add_argument("--log-path", type=Path, default=None, help="Optional LaTeX log path to inspect for post-build failures.")
    parser.add_argument("--rendered-qa-path", type=Path, default=None, help="Rendered-page PDF QA record for final bundle status.")
    parser.add_argument("--final", action="store_true", help="Require final bundle gates: PDF, LaTeX log, and rendered-page QA.")
    args = parser.parse_args()

    result = audit_tex(
        args.tex_path,
        pdf_path=args.pdf_path,
        log_path=args.log_path,
        rendered_qa_path=args.rendered_qa_path,
        final_mode=args.final,
    )
    report_path = args.report or args.tex_path.with_name("tables_figures_format_audit.md")
    write_report(result, report_path)
    return 0 if result.passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
