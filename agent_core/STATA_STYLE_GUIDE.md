# Stata Style Guide

This guide defines required Stata conventions for reproducible empirical execution and audit.

## Required Do-File Header

Every executable do file must include:

- Purpose.
- Required inputs.
- Generated outputs.
- Maintainer.
- Last updated date.
- Stata version.
- Package dependencies.
- Log path.
- Run order position.

## Required Do-File Setup

Every executable do file must include:

```stata
version 18
clear all
set more off
```

The Stata version may differ by project, but it must be explicit.

Every executable do file must open a log near the beginning:

```stata
log using "${log_dir}/example.log", replace text
```

Logs must be closed at the end:

```stata
log close
```

## Stata Execution Runner

When Stata is the project main language, official empirical execution must use the `stata-execution-runner` skill. The runner must prefer a configured `stata-mcp` channel when available and authorized, then fall back to local Stata batch execution such as `StataMP-64.exe /e do <file.do>`.

Python, R, or spreadsheet outputs must not replace official Stata results when Stata is available unless the researcher explicitly approves a temporary substitute. Such outputs must be labeled as validation or cross-check artifacts, not official Stata tables.

Official regression tables should be exported through `esttab` / `estout` by default. If `esttab` / `estout` is unavailable, the workflow must stop with a user-facing Stop Message or obtain approval for installation or a native Stata fallback export.

## External Ado Path Rules

For Windows/Stata projects, the default approved PLUS path is `<LOCAL_PATH>` unless the researcher explicitly approves another path. Environment-check do files and official execution do files must configure this PLUS path before any package lookup, package installation, package use, or table export command, including `which esttab`, `which estout`, `esttab`, `estout`, and `ssc install`.

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
capture which estout
which estout
```

The `sysdir` output must appear in the Stata log. Package availability checks such as `which esttab` and `which estout` must occur after `sysdir set PLUS`, not before. `capture which esttab` may be used for `_rc` failure detection, but successful official runs must also execute non-captured `which esttab` and `which estout` so the log displays the resolved `esttab.ado` and `estout.ado` paths. If a prior run failed because `esttab` was invisible before the PLUS directory was configured, rerun with the approved PLUS path before marking the package unavailable.

The latest complete Stata log overrides stale blocker records. If the latest environment-check log or official execution log shows `sysdir set PLUS "<LOCAL_PATH>"`, followed by successful non-captured `which esttab` and `which estout` resolving to ado paths under the approved PLUS directory, the table-export environment must be marked `passed`. The agent must then update or clear related P0/status records such as `review/regression_execution_blocker.md`, `review/stata_execution_runner_report.md`, and `review/P0_status.md` before using them in a Stop Message.

The agent must not continue to report `esttab` / `estout` as P0 based only on an older `P0 open`, `blocked`, or first-failure record when a newer complete log proves the approved PLUS path and both package lookups succeeded. If a historical blocker conflicts with the latest log, update the blocker/risk/gate records or explicitly state in the Stop Message that the old blocker was cleared by the latest log.

`esttab` / `estout` may remain P0 only when the latest relevant log is missing or incomplete, does not run `sysdir set PLUS "<LOCAL_PATH>"` before package checks, still fails `which esttab` or `which estout`, or resolves ado files outside the approved PLUS path without researcher approval.

## Path Rules

- All paths must use project globals.
- Raw-data paths must be read-only inputs.
- Derived-data paths must be separate from raw data.
- Output paths must be deterministic and stable.
- Avoid absolute user-specific paths inside reusable project scripts.
- Do not silently overwrite important outputs unless versioning or replacement is explicitly documented.

## Data Handling Rules

- Preserve raw data.
- Save cleaned or constructed data under controlled derived directories.
- Document recodes, type conversions, missing-value rules, and sample restrictions.
- Any sample-changing step must include before-and-after `count`.
- Key variables should be summarized after construction.
- Constructed variables should be labeled when labels are known.

Example pattern:

```stata
count
* approved sample restriction here
count
summarize <approved_constructed_variable>
```

## Key and Merge Checks

Primary keys must be checked with one of:

```stata
isid <approved_key_fields>
duplicates report <approved_key_fields>
```

Every key merge must:

- State the approved merge keys.
- Report `_merge`.
- Decide and document how unmatched observations are handled.
- Include counts before and after merge.

Example pattern:

```stata
count
merge <approved_merge_type> <approved_key_fields> using "${derived_dir}/<approved_using_dataset>.dta"
tab _merge
count
```

Do not drop `_merge` before its distribution is logged.

## Regression Code Rules

- Baseline, event-study, robustness, heterogeneity, and mechanism-related blocks must be clearly separated.
- Every regression must map to a `spec_id`.
- Every regression must explicitly show sample filters, controls, fixed effects, clustering, weights, and estimator.
- All fixed effects must be explicit in code.
- All clustering must be explicit in code.
- For commands that support these options, write `absorb(...)` and `vce(cluster ...)` explicitly.
- Do not alter controls, fixed effects, clustering, or samples inside a run unless a new approved spec exists.

Regression commands may use different Stata packages by project, but the executed command must make the approved fixed effects and clustering visible in the do file and log.

## Event Study Rules

- Event-time construction must be approved and logged.
- Window and omitted period must be approved before execution.
- Sparse bins or collapsed tails must be documented.
- Figures must be generated from stored coefficients or reproducible graph commands.

## Failure Handling

Any failed regression must be recorded in `failed_regressions.md` with:

- `spec_id`.
- Do file.
- Log file.
- Error message or return code.
- Whether any output was produced.
- Current status: failed, blocked, needs author input, or rerun required.

A failed regression must not appear in final tables as a successful result.

## Logs Must Capture

- Do-file start and end.
- Stata version and relevant package versions where practical.
- Data paths loaded and outputs written.
- Key counts before and after sample changes.
- Key and duplicate checks.
- Merge diagnostics, including `_merge`.
- Variable construction summaries.
- Regression commands and output.
- Export commands and output paths.
- Errors and return codes.

## Style Preferences

- Use stable macro names for directories.
- Use stable estimate names for models.
- Keep one responsibility per do file when practical.
- Keep comments factual and operational.
- Avoid manuscript interpretation in comments.
