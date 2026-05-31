---
name: tables-figures-format
description: Audit final Tables and Figures plus Appendix LaTeX/PDF layout for centered notes, decimal precision, main-table page breaks, Appendix placement, duplicate table numbers, placeholders, and compile readiness.
---

# tables-figures-format

## when_to_use
Use before compiling a final `Tables and Figures` plus `Appendix` PDF, before marking a bundle final, and before copying any bundle into handoff main evidence.

## required_checks
- No duplicate table-number captions such as `Table 1: Table 1. Descriptive Statistics`.
- No mixed Chinese/English duplicate table-number captions such as `表 1: Table 1. Descriptive Statistics`.
- Table 2 and later main tables are preceded by `\clearpage` or `\newpage` unless compact version is explicitly approved.
- Appendix appears after the final main table or figure.
- Appendix is preceded by `\clearpage`.
- Appendix title is centered.
- Appendix Table A starts on the same page as the Appendix title; no `\clearpage` or `\newpage` appears between them.
- Notes are centered or inside a centered `threeparttable`/`tablenotes` block.
- Final LaTeX tables use `booktabs` three-line structure: `\toprule`, `\midrule`, and `\bottomrule`.
- Descriptive statistics and model outputs use approved numeric precision.
- No raw long decimals remain in final display output.
- No unresolved placeholders remain.
- LaTeX logs contain no hard failures such as `Float too large`, fatal errors, or unresolved compilation errors.
- PDF exists and rendered-page QA status is recorded. If rendering tools are unavailable, the missing rendered-page QA status blocks final bundle status and must be reported as an environment blocker.

## default_numeric_precision
- `N`: 0 decimals.
- `Mean`, `SD`, `Min`, `P25`, `Median`, `P75`, `Max`: 3 decimals.
- Correlation: 3 decimals.
- Regression coefficients: 3 decimals.
- Standard errors: 3 decimals.
- p-values: 3 decimals, or omit separate p-values when significance stars are used.

Integer or categorical variables may use 0 or 1 decimals only when the table-generation logic applies that exception consistently and documents it.

## required_outputs
- `tables_figures_format_audit.md` whenever the audit is run.
- Failed audit status if any required check fails.

## script
Use:

```bash
python scripts/tables_figures_format_check.py <path-to-tex> --report <path-to-tables_figures_format_audit.md> --pdf-path <path-to-compiled-pdf> --log-path <path-to-latex-log>
```

Use the command without `--pdf-path`, `--log-path`, `--rendered-qa-path`, and `--final` for static preflight before compilation. For final bundle or handoff status, rerun the final gate:

```bash
python scripts/tables_figures_format_check.py <path-to-tex> --final --report <path-to-tables_figures_format_audit.md> --pdf-path <path-to-compiled-pdf> --log-path <path-to-latex-log> --rendered-qa-path <path-to-rendered-pdf-qa.md>
```

Final gate status must report `static_tex_audit_status`, `latex_log_audit_status`, `pdf_existence_status`, and `pdf_rendered_qa_status`. If the script is unavailable, perform an equivalent static and post-build audit and write the same report fields.

## blocking_rule
If the format audit fails:

- Do not mark the `.tex` or PDF as final.
- Do not include the bundle in the handoff package main evidence.
- Record every failure in `tables_figures_format_audit.md`.
- Continue only after the `.tex` is corrected and the audit reruns cleanly.
