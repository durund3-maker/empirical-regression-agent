---
name: baseline-regression
description: Execute approved baseline regression workflows from confirmed regression specs with explicit fixed effects, clustering, logs, exports, and failure records. Use only after spec audit passes; no log, no claim.
---

# baseline-regression

## name
baseline-regression

## description
Use this skill to generate and execute the main baseline regression workflow only from confirmed `regression_specs.yml` records. When the project main language is Stata, call `stata-execution-runner` for official execution and table export. All regressions must explicitly show fixed effects and clustering, including `absorb()` and `vce(cluster ...)` when supported, and every result must have a complete log. No log, no claim.

## when_to_use
Use after regression-spec audit passes and the user asks to run or package baseline regressions from approved specifications.

## required_inputs
- Confirmed `regression_specs.yml` with baseline spec IDs.
- Approved analysis data, variable dictionary, and sample-flow records.
- Stata do files or permission to generate approved baseline do-file scaffolds.
- Required packages and environment notes, including `esttab` / `estout` availability for official Stata tables.

## required_outputs
- `output/tables/baseline_regression.*`
- `output/logs/baseline_regression.log`
- `review/baseline_regression_run_report.md`
- `review/failed_regressions.md`

## workflow
1. Confirm that the regression-spec audit has no open P0 blockers for baseline specs.
2. Confirm that each approved spec has a Fixed Effects Decision Node comparing `TWFE vs mixed regression`, with no-FE allowed only for a documented technical exception.
3. Generate or execute baseline do files with required Stata header, project globals, `version`, `clear all`, `set more off`, and `log using`.
4. Ensure every regression maps to a `spec_id` and explicitly records outcome, key regressor, controls, sample condition, fixed effects, cluster, weights, and estimator.
5. Use explicit `absorb(...)` and `vce(cluster ...)` where the command supports them.
6. For Stata-primary projects, route official execution through `stata-execution-runner`; prefer configured `stata-mcp`, then local Stata batch execution as fallback.
7. Export baseline tables through Stata `eststo` plus `esttab` / `estout` by default; never hand-fill numbers.
8. Treat Python/R outputs as validation or cross-check artifacts only unless the researcher explicitly approves them as a temporary non-Stata substitute.
9. If a regression fails, record `spec_id`, do file, log, error or return code, output status, and next action in `failed_regressions.md`.
10. Write a run report linking specs, scripts, logs, outputs, failures, and audit status.

## forbidden_actions
- Do not change fixed effects, clustering, controls, samples, weights, or estimators without a new confirmed spec.
- Do not add or remove variables to obtain significance.
- Do not treat failed or partially executed regressions as successful.
- Do not manually edit coefficients, standard errors, p-values, stars, or sample sizes.
- Do not write causal manuscript conclusions.
- Do not silently replace official Stata baseline results with Python/R results when the project main language is Stata and Stata is available.

## human_review_checkpoint
Researcher confirmation is required before execution for main specification, fixed effects, clustering, controls, estimator, weights, sample filter, and how to handle unexpected failures or sample deviations.

## P0_risks
- Baseline spec is unconfirmed.
- Fixed Effects Decision Node is missing or lacks the `TWFE vs mixed regression` comparison.
- No-FE baseline is proposed without one of the documented technical exceptions and researcher confirmation.
- Required log is missing or incomplete.
- Main language is Stata but official baseline results are produced only by Python/R without explicit validation/cross-check labeling.
- `esttab` / `estout` is required for official Stata table export but missing, and no approved fallback is recorded.
- Failed regression is not recorded.
- Table cannot be traced to spec, do file, log, and output.
- Approved FE, cluster, controls, or sample are changed.

## P1_risks
- Sample size differs materially from expectation.
- Runtime package versions differ from target environment.
- Non-core formatting remains pending after numerical output is traceable.

## expected_files
- `regression_specs.yml`
- Baseline do file and, when Stata is the main language, Stata-generated official table export through `esttab` / `estout` unless an approved fallback is recorded.
- `output/tables/baseline_regression.*`
- `output/logs/baseline_regression.log`
- `review/baseline_regression_run_report.md`
- `review/failed_regressions.md`

## evidence_requirements
Baseline result claims require approved spec, executable do file, complete log, exported table, and audit status. No log, no claim.

## audit_trail_requirements
Record run date, software environment, spec IDs, script paths, log paths, output paths, return codes, failures, rerun requirements, and P0/P1/P2 status.
