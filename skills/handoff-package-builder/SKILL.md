---
name: handoff-package-builder
description: Assemble audited empirical artifacts, logs, scripts, inventories, evidence maps, failure records, and risk reports into a handoff package. Use after audits to package materials for researcher review or approved empirical-paper-agent transfer without writing manuscript prose.
---

# handoff-package-builder

## name
handoff-package-builder

## description
Use this skill to assemble a reproducible handoff package for downstream review or possible transfer to `empirical-paper-agent`. It packages audited empirical artifacts, logs, scripts, inventories, evidence maps, failure records, and risk reports without writing manuscript prose, changing empirical results, or upgrading agent inference into verified evidence.

## when_to_use
Use after regression audit and table-output audit when the user asks to build, inspect, or update a handoff package.

## required_inputs
- Passed or explicitly disclosed audit records.
- Tables, figures, logs, do files, variable map, table inventory, sample flow, evidence map, run reports, failed-regression records, P0/P1/P2 status reports.
- Researcher decision about whether transfer to `empirical-paper-agent` is approved.

## required_outputs
- `handoff_package/`
- `handoff_package/handoff_README.md`
- `handoff_package/file_manifest.csv`
- `review/handoff_package_audit.md`

## workflow
1. Verify there are no open P0 blockers before marking handoff complete.
2. Run or document the final status convergence gate. Use `scripts/status_convergence_check.py` when available. If review, bundle, approval, transfer, proposal/executed/final, or TODO statuses conflict, stop and write a blocking status report.
3. Run or document the encoding gate. Use `scripts/encoding_check.py` when available. If packaged text artifacts contain mojibake or are not UTF-8 readable, exclude or correct them before handoff.
4. Verify every packaged regression table either passed the regression table hard gate or is clearly labeled as appendix diagnostic/excluded. Hard-gated tables cannot enter main evidence.
5. Run or document the Tables/Figures format gate for any combined `.tex` or PDF bundle. Use `scripts/tables_figures_format_check.py --final --pdf-path --log-path --rendered-qa-path` when available. Final handoff main evidence requires `static_tex_audit_status=passed`, `latex_log_audit_status=passed`, `pdf_existence_status=passed`, and `pdf_rendered_qa_status=passed`. If the audit fails or rendered-page QA is missing, failed, pending, or `environment_blocker`, generate `tables_figures_format_audit.md` and exclude the bundle from handoff main evidence.
6. Assemble or index required package components: `tables/`, `figures/`, `logs/`, `do/`, `variable_map.csv`, `table_inventory.csv`, `sample_flow.csv`, `evidence_map.csv`, `regression_run_report.md`, `failed_regressions.md`, `P0_status.md`, `P1_risks.md`, `final_regression_audit.md`, and `handoff_README.md`.
7. Build `variable_map.csv` only from `executed_variable_dictionary.csv`. Do not copy proposal-only dictionaries into handoff.
8. Preserve empirical outputs as generated; do not edit numerical results or specifications.
9. Create `file_manifest.csv` with path, role, source, evidence class, audit status, and risk level.
10. Write `handoff_README.md` with purpose, directory map, run order, key artifact Markdown links, relative `Path:` lines, absolute `Absolute Path:` lines, software requirements, reproduction notes, evidence rules, Tables/Figures audit sub-statuses, and transfer status.
11. Write `handoff_package_audit.md` documenting completeness, missing files, P0/P1/P2 status, status convergence, encoding audit, regression hard-gate results, Tables/Figures format audit, variable-map provenance, and remaining risks.
12. If transfer is not separately approved, mark the package as prepared for researcher review only.

## forbidden_actions
- Do not write manuscript body text.
- Do not modify empirical results, specifications, table numbers, or logs.
- Do not omit failed regressions or unresolved risks.
- Do not present agent inference as verified evidence.
- Do not transfer to `empirical-paper-agent` without explicit researcher confirmation.
- Do not mark handoff complete when final status records conflict.
- Do not include proposal-only, pending, not-executed, or unverified variable rows in the handoff variable map.
- Do not include mojibake-damaged text artifacts in final handoff.
- Do not package hard-gated regression tables as main evidence.
- Do not package a combined Tables/Figures bundle as main evidence when `tables_figures_format_audit.md` reports unresolved failures, the LaTeX log audit fails, PDF existence is not confirmed, or rendered-page QA is missing.

## human_review_checkpoint
Researcher confirmation is required for final handoff status and any transfer to `empirical-paper-agent`.

## P0_risks
- Handoff lacks required core artifacts.
- Open P0 blocker remains.
- Failed regressions are omitted.
- Evidence map upgrades unverified claims or agent inference to verified evidence.
- Status convergence check finds conflicting complete/pending/proposal/not-approved/not-built states.
- Encoding audit finds mojibake or non-UTF-8 packaged text artifacts.
- Handoff variable map derives from proposal-only or pending dictionary rows.
- A hard-gated pathological regression table is included as main evidence.
- A combined Tables/Figures bundle with unresolved format-audit failures, LaTeX log hard failures, missing PDF, or missing rendered-page QA is included as main evidence.

## P1_risks
- Known limitations are not prominent enough.
- P1 risk register is incomplete.
- Package is complete but navigation or reproduction instructions need researcher review.

## expected_files
- `handoff_package/tables/`
- `handoff_package/figures/`
- `handoff_package/logs/`
- `handoff_package/do/`
- `handoff_package/variable_map.csv`
- `handoff_package/table_inventory.csv`
- `handoff_package/sample_flow.csv`
- `handoff_package/evidence_map.csv`
- `handoff_package/regression_run_report.md`
- `handoff_package/failed_regressions.md`
- `handoff_package/P0_status.md`
- `handoff_package/P1_risks.md`
- `handoff_package/final_regression_audit.md`
- `handoff_package/handoff_README.md`
- `handoff_package/file_manifest.csv`
- `review/handoff_package_audit.md`

## evidence_requirements
Each packaged status claim must cite supporting artifacts and retain evidence class. Verified evidence requires approved input, executable script, complete log, output, and passed audit.

## audit_trail_requirements
Record package build date, included files, omitted files, evidence classes, audit statuses, open risks, transfer approval status, and required next actions.
