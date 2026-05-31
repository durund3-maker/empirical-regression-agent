---
name: stata-execution-runner
description: Execute approved Stata do files through stata-mcp when available or local Stata batch mode as fallback, verify esttab/estout for official tables, capture logs, and prevent Python/R substitution for official Stata results.
---

# stata-execution-runner

## name
stata-execution-runner

## description
Use this skill as the required execution entry point whenever a project's main language is Stata and an approved workflow needs descriptive statistics, regressions, mechanism checks, robustness checks, or official table export. It discovers the Stata execution channel, checks package readiness, runs only approved do files, captures logs and return codes, and preserves the rule that official Stata results cannot be silently replaced by Python/R output.

This skill is inspired by the `stata-mcp` pattern: use an MCP-backed Stata session first when it is configured and reachable, otherwise fall back to local Stata batch execution such as `StataMP-64.exe /e do <file.do>` on Windows.

## when_to_use
Use before or inside `baseline-regression`, `descriptive-statistics`, `event-study`, `robustness-checks`, `heterogeneity-mechanism`, and Stata table-export workflows when Stata is the primary project language.

## required_inputs
- Project metadata identifying the main language and target Stata version.
- Approved do file path and working directory.
- Approved spec or table-plan record covering outcome, treatment, controls, sample, fixed effects, clustering, estimator, and output paths.
- Expected Stata executable path or configured `stata-mcp` endpoint when available.
- Expected log path and official table output path.

For Windows local batch fallback, default to a working-directory-first command strategy:

- `cd /d` to the approved project root first.
- Pass the do file as a relative path from the project root when possible.
- Quote every path.
- Avoid passing a full do-file path with spaces directly to Stata.
- Generate a command preview before execution.
- Save the full command preview, working directory, do-file path, expected log path, and return code to a command log.

## required_outputs
- Complete Stata log for every executed do file.
- Return-code or run-status record with separate `process_status`, `log_status`, `stata_error_status`, and `table_export_status`.
- Official Stata-generated output table when table export is in scope.
- Failure record when Stata execution, package checks, or table export fails.
- User-facing Stop Message when execution cannot proceed.

## execution_priority
1. Prefer configured `stata-mcp` when reachable and authorized. Use it to run approved do files and capture Stata output.
2. If MCP is unavailable, use local Stata batch mode from the configured project path or discovered executable path.
3. If Stata is unavailable, stop and produce a Stop Message. Do not use Python/R as an official replacement.

## preflight_checks
Before running analysis, verify and record:

- Project main language is Stata when official Stata results are required.
- Stata version and executable channel are known.
- For Windows/Stata projects, use `<LOCAL_PATH>` as the default approved PLUS path unless the researcher explicitly approves another path. Set it before package checks, package installation, package use, or table export commands, then run `sysdir` so the configured ado paths appear in the Stata log.
- Working directory, do file path, log path, and output table path are inside the approved project workspace.
- Approved spec contains estimator, sample, controls, fixed effects, clustering, and output scope.
- `sysdir set PLUS "<LOCAL_PATH>"` must run before package checks. `capture which esttab` is used only for failure detection. After a successful check, non-captured `which esttab` and `which estout` must run so the resolved `esttab.ado` and `estout.ado` paths are written to the Stata log.
- If `esttab` / `estout` is missing, stop with a user-facing Stop Message or request approval for installation or a native Stata fallback export.

## ado_path_preflight
The runner must treat the approved Stata external-command directory as part of the execution environment rather than as a project-specific workaround. The do file or environment-check do file must set the PLUS path before any package lookup, package installation, package use, or table export command:

```stata
sysdir set PLUS "<LOCAL_PATH>"
sysdir
capture which esttab
if _rc {
    display as error "P0: esttab/estout is not installed or not visible to Stata."
    log close
    exit 499
}
which esttab
which estout
```

If `which esttab` fails before this preflight has run, the run is not a valid package-readiness check. Rerun after setting the approved PLUS directory. `capture which` is not enough for audit evidence because it suppresses the resolved ado path; successful package checks must record ado path output through non-captured `which esttab` and `which estout`.

## stale_blocker_reconciliation
Before producing a Stop Message for missing `esttab` / `estout`, the runner must inspect the latest relevant complete Stata log. If that log shows `sysdir set PLUS "<LOCAL_PATH>"` followed by successful non-captured `which esttab` and `which estout` resolving to ado paths under the approved PLUS directory, the table-export environment is passed and old blocker records are stale.

When the latest log proves the package check passed, update or clear stale records such as `review/regression_execution_blocker.md`, `review/stata_execution_runner_report.md`, and `review/P0_status.md` before reporting current status. Do not let an older `P0 open`, `blocked`, first-failure record, or stale blocker file override a newer successful log.

Keep `esttab` / `estout` as P0 only when the latest relevant log is missing or incomplete, does not set the approved PLUS path before package checks, still fails `which esttab` or `which estout`, or resolves ado files outside the approved PLUS path without explicit researcher approval.

## execution_status_convergence
The runner must not collapse process status and empirical execution status into one success/failure flag.

- `process_status` records command-layer status such as `passed`, `failed`, `timeout`, or `not_run`.
- `log_status` records whether the latest Stata log is missing, present but unparsed, complete success, or complete failed.
- `stata_error_status` records whether parsed Stata errors passed, failed, or were not checked.
- `table_export_status` records whether required official table outputs exist and are linked to the run.
- If `process_status=timeout` but `log_status=complete_success`, `stata_error_status=passed`, and `table_export_status=passed` or `not_applicable`, the run status is `completed_with_runner_warning`.
- `completed_with_runner_warning` may clear stale P0 blockers that contradict the latest complete successful log, but the runner warning must remain in `review/stata_execution_runner_report.md`, handoff risks, or the command log.
- A failed latest complete log remains P0 even if the process returned zero.

## workflow
1. Inspect project metadata and approved specs to confirm Stata is the official execution language.
2. Select execution channel: `stata-mcp` first, local Stata batch second.
3. Run a lightweight package/environment check: set the approved PLUS path, record `sysdir`, use `capture which esttab` only to detect failure, then run non-captured `which esttab` and `which estout` to record ado paths for official table workflows.
4. Execute only approved `.do` files; do not paste ad hoc model commands outside the approved script. On Windows local batch, use `cmd.exe /c cd /d "<project_root>" && "<stata_path>" /e do "<relative_do_file>"`.
5. Capture complete logs, return status, output paths, any Stata error code, and the four status fields `process_status`, `log_status`, `stata_error_status`, and `table_export_status`.
6. Verify output tables exist and were produced by the logged Stata run.
7. Write or update run reports and failed-regression records.

## forbidden_actions
- Do not use Python, R, spreadsheet formulas, or hand entry as the official result source when Stata is available and configured as the main project language.
- Do not silently downgrade official Stata execution to Python/R. Python/R output may only be labeled as validation or cross-check with explicit user approval.
- Do not run unapproved do files or alter approved FE, clustering, controls, sample, estimator, or table scope.
- Do not mark a Stata run successful if the log is missing, incomplete, or has an unresolved error.
- Do not treat a table as official when `esttab` / `estout` was required but unavailable.
- Do not report `esttab` / `estout` as currently unavailable from stale blocker files when the latest complete Stata log shows successful `which esttab` and `which estout` after `sysdir set PLUS "<LOCAL_PATH>"`.
- Do not execute Windows local batch by passing an unquoted full do-file path with spaces directly to Stata.

## stop_message_contract
If the runner stops, the final user-visible reply must use the fixed `## Stop Message` template:

Keep fixed field names in English, but write field values in Chinese whenever practical. Keep paths, commands, package names such as `esttab` / `estout`, `.do` filenames, log paths, model names, and other technical identifiers in their original form. This Chinese-language rule does not apply to formal tables, figures, table notes, figure notes, captions, labels, legends, or LaTeX/RTF/XLSX output.

```markdown
## Stop Message

- why stopped: <用中文说明 exact Stata runner blocker, package/export blocker, execution failure, approval boundary, or approved-scope boundary>
- current status: <用中文说明 Stata MCP status, local Stata batch status, Stata path checked, esttab/estout status, do/log/output files checked, and records generated or updated>
- current problems:
  - P0: <用中文说明 missing Stata executable or MCP channel, missing esttab/estout when required, missing/incomplete log, failed execution, official evidence boundary, or none>
  - P1: <用中文说明 environment/version/package caution or recoverable output-format issue, or none>
  - P2: <用中文说明 minor formatting/documentation issue, or none>
- questions for researcher:
  1. <如果 Stata 缺失，用中文要求提供或确认 Stata executable path>
  2. <如果 esttab/estout 缺失，用中文要求批准安装 `estout`、批准 native Stata fallback export，或确认其他 approved table-export path>
  3. <如相关，用中文确认任何 temporary non-Stata output 是否只能作为 validation/cross-check，而不是 official Stata evidence>
- blocked boundary: <用中文说明用户回复前哪些内容不能运行、导出或视为 official evidence>
- required user action: <用中文说明需要的 path、installation approval、fallback approval、rerun decision、corrected do file/log 或 evidence-class decision>
- next action after response: <用中文说明将 retry Stata MCP/local batch execution、install/use approved export path、rerun do file 或 record blocked status>
- project record paths: <review/stata_execution_runner_report.md, failed_regressions.md, do/log/output paths, or expected record paths>
```

If there are no current problems or no researcher questions, write `current problems: none` or `questions for researcher: none` explicitly. P1/P2 issues do not stop Stata execution by themselves, but they must be disclosed if the runner stops for another reason.

## P0_risks
- Main language is Stata but official results are generated only by Python/R without explicit cross-check labeling.
- Stata executable or MCP channel is missing and no Stop Message is produced.
- `esttab` / `estout` is required but missing and no approval is obtained for installation or fallback.
- Do file, log, and output table are not traceably linked.
- Failed Stata execution is not recorded.

## P1_risks
- Stata package versions differ from target environment but outputs are reproducible.
- MCP is unavailable but local batch execution succeeds.
- Table formatting needs cleanup while numerical output remains traceable.
- LaTeX and RTF companion outputs differ only in formatting while sharing the same Stata estimates.

## evidence_requirements
Official Stata evidence requires an approved spec, approved do file, complete Stata log, Stata-generated table output, and audit status. LaTeX `.tex` is the preferred official manuscript table format when requested; `.rtf` may be generated as a companion review format. Python/R artifacts can support validation only when explicitly labeled as cross-checks.

## audit_trail_requirements
Record execution channel, Stata executable or MCP endpoint, configured ado PLUS path, `sysdir` output, Stata version, package check results, resolved `esttab.ado` and `estout.ado` paths, do file path, working directory, log path, output table path, return code, failed commands, and whether any non-Stata cross-check artifacts exist.
