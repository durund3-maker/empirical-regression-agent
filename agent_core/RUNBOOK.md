# Runbook

This runbook defines the default operating order for a concrete empirical project. It assumes a project workspace already exists and has been approved by the researcher. It must not be used to create manuscript prose.

## 1. Confirm Project Boundary

1. Confirm the project directory, owner, and output scope.
2. Confirm that raw data are read-only.
3. Confirm software requirements, including Stata version and required packages.
4. Confirm whether the task is execution, audit, export, replay, or handoff.

Stop if project metadata or raw-data locations are unavailable.

## 2. Build Material Map

1. Inventory raw data, derived data, scripts, logs, tables, figures, notes, and config files.
2. Classify each artifact as raw input, derived input, executable source, output, audit record, or author note.
3. Record provenance and path stability.
4. Mark missing or ambiguous files as open risks.

Do not treat files with unknown provenance as verified evidence.

## 3. Validate Metadata and Schemas

1. Fill or audit `project_metadata`.
2. Validate data-source entries.
3. Validate or draft `regression_specs`.
4. Validate or draft `robustness_matrix`.
5. Validate `table_output` expectations.
6. Initialize `audit_status` records for major artifacts.

Schema fields may be marked `unknown` or `needs_author_input`; do not fill empirical content by invention.

## 4. Data Audit Before Cleaning

1. Check raw file readability.
2. Inspect variable names and labels against dictionaries.
3. Check primary keys using `isid` or `duplicates report` in Stata where applicable.
4. Summarize missingness and variable ranges.
5. Identify merge candidates and merge risks.

Stop if key files are unreadable or raw data appear modified.

## 5. Cleaning Proposal

1. Draft sample-screening rules.
2. Draft recodes, missing-value handling, type conversions, and derived-data paths.
3. Draft winsorization, trimming, or outlier handling only when requested by the researcher.
4. Define before-and-after `count` checks for every sample-changing step.
5. Ask for researcher confirmation.

Do not execute unapproved cleaning rules.

## 6. Variable Construction Proposal

1. Map each variable to source field, formula, unit, label, and missing-value rule.
2. Identify required intermediate variables.
3. Define post-construction validation: `summarize`, tabulations, range checks, and dictionary updates.
4. Ask for researcher confirmation.

Do not construct undocumented proxies or substitute variables.

## 7. Write or Review Executable Scripts

1. Use project globals for all paths.
2. Include `version`, `clear all`, `set more off`, and `log using`.
3. Use deterministic output names.
4. Include key counts, merge diagnostics, duplicate checks, and summaries.
5. Separate cleaning, variable construction, descriptive outputs, regressions, and exports where practical.

Do not create Stata code that silently overwrites outputs without logs or versioned backups.

## 8. Run Cleaning and Variable Construction

1. Execute approved scripts.
2. Save logs.
3. Verify derived data paths.
4. Update variable map and sample-flow records.
5. Record failures or unexpected sample changes.

Stop if scripts fail or sample changes cannot be explained by approved rules.

## 9. Generate Descriptive Outputs

1. Run descriptive tables and figures from approved data.
2. Export outputs using stable names.
3. Link each output to scripts and logs.
4. Update table and figure inventories.

Do not interpret descriptive outputs as causal evidence.

## 10. Baseline Regression Proposal and Gate

1. Draft or audit baseline `regression_specs`.
2. Confirm dependent variable, key variable, controls, fixed effects, clustering, estimator, weights, and sample filter.
3. Confirm expected table columns and output formats.
4. Ask for researcher confirmation.

Baseline execution is P0-blocked until confirmed.

## 11. Run Baseline Regressions

1. Execute only approved specs.
2. Ensure every model explicitly logs fixed effects, clustering, controls, and sample.
3. Store estimates with stable names.
4. Export tables directly from Stata output.
5. Record failed models in `failed_regressions.md`.

Do not change models during execution to improve significance.

## 12. Run Event Study, Robustness, Heterogeneity, and Mechanism-Related Tasks

1. Confirm event-study window and omitted period.
2. Confirm robustness matrix.
3. Confirm subgroup definitions and mechanism-related designs.
4. Execute approved tasks.
5. Export outputs and update inventories.
6. Label evidence type precisely.

Do not present heterogeneity as mechanism unless the researcher has explicitly documented that design.

## 13. Export Tables and Figures

1. Export tables in approved formats, prioritizing `rtf`, `tex`, and `xlsx`.
2. Prefer three-line table style when supported.
3. Ensure notes state FE, clustering, controls, sample, and stars.
4. Remove unintended blank statistic rows.
5. Ensure titles and column labels match actual specs.

Do not manually fill or edit numerical results.

## 14. Audit Regression Outputs

1. Match each table column to a spec ID.
2. Match each spec ID to source do files and logs.
3. Verify sample, FE, clustering, controls, estimator, weights, and output path.
4. Check failed-regression records.
5. Classify each issue as P0, P1, or P2.
6. Write `final_regression_audit.md`.

P0 issues block completion.

## 15. Assemble Handoff Package

1. Include required directories: `tables/`, `figures/`, `logs/`, and `do/`.
2. Include required CSV and Markdown reports listed in `HANDOFF_PROTOCOL.md`.
3. Include failed regressions, P0 status, P1 risks, evidence map, and replay instructions.
4. Ask the researcher whether to hand off to `empirical-paper-agent`.

Do not transfer the package without human approval.

## 16. Replay Validation

1. Re-run or dry-run the documented run order.
2. Compare regenerated outputs against the package inventory.
3. Record environment-dependent differences.
4. Update final P0/P1/P2 status.

Replay success requires logs and traceable regenerated outputs.

## Universal Stop Conditions

Stop and report a P0 blocker when:

- A required input is missing and cannot be marked unavailable.
- Raw data were modified.
- Main regression specification is unconfirmed.
- A do file fails and no failure record is created.
- A core table cannot be traced to code and log files.
- A failed regression is being treated as successful.
- The user asks for invented empirical content or unsupported manuscript conclusions.
