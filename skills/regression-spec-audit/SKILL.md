---
name: regression-spec-audit
description: Audit regression specification files for explicit outcomes, treatments, controls, fixed effects, clustering, samples, estimators, and expected tables. Use before any regression execution to identify P0 blockers without running models.
---

# regression-spec-audit

## name
regression-spec-audit

## description
Use this skill to audit `regression_specs.yml` for completeness before any regression execution. It verifies that outcomes, treatments, controls, fixed effects, clustering, sample conditions, estimators, weights, and expected tables are explicit and confirmed. This skill does not run regressions.

## when_to_use
Use before baseline, event-study, robustness, heterogeneity, or mechanism-related execution when the user asks whether specifications are ready to run or whether a spec file has P0 blockers.

## required_inputs
- `regression_specs.yml` or the configured equivalent.
- `config/regression_specs_schema.yml`.
- Variable dictionary, sample-flow records, author notes, and approval records.
- Expected table plan or table-output schema if available.

## required_outputs
- `review/regression_spec_audit.md`
- `review/P0_regression_spec_issues.md`

## output_language
Researcher-facing Markdown prose in audit findings, P0 issue descriptions, required confirmations, and next-action instructions should be written in Chinese whenever practical. Preserve variables, formulas, field names, code, file paths, commands, Stata package names, model names, schema values, status enums, decision enums, and machine-readable blocks in their original form.

## workflow
1. Load the regression spec file and compare each record to the schema.
2. Check that outcome, treatment or key regressor, controls, fixed effects, cluster, sample condition, estimator, weights, linked variables, and expected table are explicit.
3. Check the Fixed Effects Decision Node for `TWFE vs mixed regression`: `candidate_fixed_effects`, `candidate_mixed_controls`, `selected_fe_strategy`, `rejected_fe_strategy`, and `rejection_reason`.
4. Verify that any no-FE specification documents one of the allowed technical exceptions: no usable FE dimension exists, fixed effects are fully collinear with key variables, or sample sparsity/degrees-of-freedom constraints make FE models non-estimable.
5. Verify that each model links to approved variables, sample rules, and author decisions.
6. Mark unconfirmed fixed effects, clustering, controls, sample filters, estimators, expected table mappings, or missing FE-decision records as P0.
7. Check that each `spec_id` is unique and stable.
8. Write `regression_spec_audit.md` with complete, incomplete, blocked, and pending specs.
9. Write `P0_regression_spec_issues.md` listing blockers and required author actions.

## forbidden_actions
- Do not run regressions.
- Do not choose, repair, or optimize specifications independently.
- Do not change fixed effects, clustering, controls, estimators, or samples.
- Do not infer missing controls or sample filters from prior projects.
- Do not decide whether identification is valid.

## human_review_checkpoint
Researcher confirmation is required for main specification, fixed effects, clustering, controls, sample filters, weights, estimators, and expected table mapping.

## P0_risks
- Any required spec field is missing or unconfirmed.
- Spec references undocumented variables or unapproved sample rules.
- Fixed effects, clustering, or controls are ambiguous.
- Missing `TWFE vs mixed regression` comparison in the Fixed Effects Decision Node.
- No-FE specification without a documented technical exception and researcher confirmation.
- Expected table cannot be mapped to spec IDs.

## P1_risks
- Estimator choice or weighting is documented but needs careful review.
- Model labels are clear enough for execution but not final.
- Expected sample differs from variable-construction sample.

## expected_files
- `regression_specs.yml`
- `review/regression_spec_audit.md`
- `review/P0_regression_spec_issues.md`

## evidence_requirements
Every readiness claim must cite the spec record, schema requirement, variable dictionary, sample-flow file, or author approval. Missing fields must remain gaps.

## audit_trail_requirements
Record audited spec IDs, schema version, linked files, confirmations found, P0/P1/P2 findings, and required next actions.
