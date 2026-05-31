---
name: robustness-checks
description: Execute approved robustness checks from a robustness matrix, including alternative outcomes, samples, fixed effects, clusters, estimators, placebo checks, and threshold checks. Use only for pre-approved checks, never for significance-driven selection.
---

# robustness-checks

## name
robustness-checks

## description
Use this skill to execute robustness checks only from an approved `robustness_matrix.yml`. It covers documented alternative outcomes, samples, fixed effects, clusters, estimators, placebo checks, and threshold checks without selecting results based on significance.

## when_to_use
Use after baseline results and a robustness matrix are approved when the user asks to run or audit robustness workflows.

## required_inputs
- Approved `robustness_matrix.yml`.
- Baseline spec IDs and passed or pending baseline run report.
- Approved analysis data, variable dictionary, and sample-flow records.
- Expected robustness output plan.

## required_outputs
- `output/tables/robustness_*.*`
- `output/logs/robustness_*.log`
- `review/robustness_run_report.md`
- `review/robustness_risk_flags.md`

## workflow
1. Verify that each robustness check links to a baseline spec and states its exact deviation.
2. Confirm researcher approval for the robustness matrix and any alternative outcome, sample, FE, cluster, estimator, placebo, or threshold rule.
3. Execute only checks listed in the approved matrix.
4. Log sample changes, command lines, FE, clustering, controls, estimator, output paths, and errors.
5. Export tables through executable code and map columns to robustness IDs and baseline spec IDs.
6. Record every failed robustness regression in `failed_regressions.md` or the project failure record.
7. Write run and risk reports disclosing deviations, sample shifts, failures, and P0/P1/P2 status.

## forbidden_actions
- Do not add, remove, or reorder robustness checks after seeing significance unless a new approval is recorded.
- Do not choose favorable robustness results for presentation.
- Do not change baseline-linked FE, clustering, controls, or sample except as the matrix explicitly states.
- Do not hide failed checks or omit them from reports.
- Do not hand-fill table numbers.

## human_review_checkpoint
Researcher confirmation is required for the robustness matrix and any deviations from baseline, including alternative outcomes, samples, fixed effects, clusters, estimators, placebo designs, and threshold rules.

## P0_risks
- Robustness matrix is missing or unapproved.
- Output lacks a complete log.
- Failed regression is not recorded.
- Robustness table cannot be traced to matrix, do file, log, and output.

## P1_risks
- Robustness sample changes materially relative to baseline.
- Alternative definitions or estimators require careful interpretation.
- Some non-core robustness outputs are pending audit.

## expected_files
- `robustness_matrix.yml`
- `output/tables/robustness_*.*`
- `output/logs/robustness_*.log`
- `review/robustness_run_report.md`
- `review/robustness_risk_flags.md`
- `review/failed_regressions.md` when failures exist or must be explicitly empty.

## evidence_requirements
Robustness claims require approved matrix, baseline linkage, executable code, complete log, exported table, and audit status. No log, no claim.

## audit_trail_requirements
Record robustness IDs, baseline links, approved deviations, scripts, logs, outputs, failures, sample differences, and risk flags.
