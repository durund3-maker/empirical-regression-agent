---
name: data-cleaning
description: Prepare data-cleaning proposals, sample-flow records, decision logs, and approved cleaning-script scaffolds while keeping raw data read-only. Use when cleaning rules, merge rules, recodes, deduplication, or outlier handling must be documented before execution.
---

# data-cleaning

## name
data-cleaning

## description
Use this skill to draft a reproducible data-processing proposal and cleaning-script scaffold from documented source data and approved or pending sample rules. This skill protects raw data as read-only and requires all unit, time, key, merge, deduplication, drop, keep, missing-value, unreasonable-value, winsorization, trimming, and outlier handling decisions to be documented in sample-flow and decision logs before execution.

## when_to_use
Use after data inventory audit when the user needs a cleaning plan, sample-flow design, or executable cleaning scaffold, especially before any sample-changing or merge operation.

## required_inputs
- `review/data_inventory_audit.md`
- `output/data_file_inventory.csv`
- Project metadata and author notes.
- Data dictionary and documented unit, time, key, sample, merge, recode, missing-value, unreasonable-value, outlier, event-window, multiple-treatment, control-group, and variable-construction rules if available.
- Human confirmations for any rule that changes the sample or transforms variables.

## required_outputs
- `review/data_cleaning_proposal.md`
- `config/sample_flow.csv`
- `review/cleaning_decision_log.md`

## output_language
Researcher-facing Markdown prose in proposals, decision logs, gate notes, and risk descriptions should be written in Chinese whenever practical. Preserve variables, formulas, field names, code, file paths, commands, Stata package names, model names, schema values, status enums, decision enums, and machine-readable blocks in their original form.

## workflow
1. Identify proposed cleaning inputs, derived-data outputs, and raw-data read-only paths.
2. Draft a data-processing proposal covering unit definition, time definition, primary keys, matching keys, deduplication version retention, sample boundaries, missing-value handling, unreasonable-value handling, outlier handling, variable units and scales, frequency alignment, panel balance, event windows, multiple treatment handling, control group definition, variable formulas, leads/lags, and geographic, industry, or administrative matching.
3. For each proposed rule, list source evidence, agent inference if any, affected files, expected output, and known risk.
4. Mark unconfirmed sample screening, merge, deduplication, missing handling, unreasonable-value handling, winsorization, trimming, outlier handling, variable formulas, event windows, multiple treatment rules, and control-group rules as blocked.
5. Create or update `config/sample_flow.csv` so each sample-changing step can record before count, after count, change count, approval reference, source script, log, and audit status.
6. Draft cleaning-script scaffolds only when requested and keep placeholders non-empirical until approvals exist.
7. Ensure any executable scaffold includes required Stata setup, project globals, log path, key checks, `_merge` reporting, duplicate diagnostics, and before/after counts.
8. Write `cleaning_decision_log.md` with author decisions, pending decisions, and P0/P1/P2 risks.

## forbidden_actions
- Do not modify raw data.
- Do not execute destructive or sample-changing cleaning without researcher confirmation.
- Do not drop observations, keep sub-samples, merge, deduplicate, alter missing values, handle unreasonable values, winsorize, trim, define events, define controls, or handle outliers without approved rules.
- Do not invent cleaning rules or variable recodes.
- Do not choose data-processing rules because they improve statistical significance.
- Do not write manuscript interpretation of cleaned data.

## human_review_checkpoint
Researcher confirmation is required before executing unit/time definitions, sample-screening rules, merge keys and matching rules, deduplication, recodes, missing-value handling, unreasonable-value handling, variable formulas, event windows, multiple treatment handling, control-group definitions, winsorization, trimming, outlier handling, and output paths.

## P0_risks
- Any sample-changing rule is unapproved.
- Merge keys or matching rules are unapproved.
- Raw data are overwritten or altered.
- Cleaning outputs lack logs or sample-flow records.

## P1_risks
- Cleaning choices are documented but substantively contestable.
- Missing-value rules or recodes may affect planned regressions.
- Derived-data paths or versioning are not yet stable.

## expected_files
- `review/data_cleaning_proposal.md`
- `config/sample_flow.csv`
- `review/cleaning_decision_log.md`
- Optional approved cleaning script under project `code/` or `do/`.
- Optional cleaning log under `output/logs/`.

## evidence_requirements
Every cleaning rule must cite an author decision, metadata entry, data dictionary, or audited source observation. Sample counts must come from executable logs; no log, no claim.

## audit_trail_requirements
Record each proposed and executed step, approval reference, source script, log path, before/after counts, output path, failure status, and unresolved risk.
