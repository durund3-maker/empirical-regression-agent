---
name: variable-construction
description: Design and audit variable-construction workflows with formulas, source fields, units, levels, timing, missing rules, validation checks, and logs. Use when documented variables must be made regression-ready without inventing or tuning definitions.
---

# variable-construction

## name
variable-construction

## description
Use this skill to design and audit variable-construction workflows from documented source fields. Each variable must record formula, source variables, unit, level, timing, and missing-value rule, and constructed variables must be validated with summaries, tabulations, or missingness reports. This skill must never adjust variables based on statistical significance.

## when_to_use
Use after cleaning rules are approved or when the user asks to prepare variable definitions, construction scripts, variable dictionaries, or audits for regression-ready variables.

## required_inputs
- Approved or proposed cleaning outputs and sample rules.
- Data dictionary, author notes, and documented variable requirements.
- Source data inventory and source fields.
- Researcher confirmation for formulas, source fields, units, missing rules, and timing.

## required_outputs
- `output/proposal_variable_dictionary.csv`
- `output/executed_variable_dictionary.csv`
- `handoff_package/variable_map.csv` only after handoff approval and only from executed variables.
- `review/variable_construction_proposal.md`
- `review/variable_construction_audit.md`

## workflow
1. List requested variables and map each to documented source fields.
2. For each questionnaire source field, complete a codebook audit before construction: question type, code meaning, whether code values are real quantities/time or option order, Likert direction, missing-value meaning, multi-select semantics, skip logic, reverse coding, and whether sum/mean/index construction is allowed.
3. Write `proposal_variable_dictionary.csv` for proposed variables only. Rows may have `approval_status=pending` and `evidence_class=proposal`, but these rows cannot enter regression or handoff.
4. Mark variables with unconfirmed formulas, undocumented sources, ambiguous coding direction, ambiguous multi-select missingness, or cascade codes used as real timing as P0 until confirmed or downgraded to descriptive-only.
5. Draft or update construction workflow using project globals, read-only inputs, derived-data outputs, and complete logs.
6. After approved execution, require `summarize`, `tab`, missingness checks, or equivalent validation for constructed variables.
7. Write `executed_variable_dictionary.csv` only for variables actually generated and validated. Each row must link source files, construction script, log, validation output, approval reference, audit status, and evidence class.
8. Build final `handoff_variable_map.csv` or `handoff_package/variable_map.csv` only from executed dictionary rows with approved or passed audit status.
9. Write `variable_construction_audit.md` with passed checks, failures, proposal-only rows, executed rows, and risk flags.

## forbidden_actions
- Do not invent variables, proxies, formulas, units, timing, or missing rules.
- Do not reverse-engineer variables to obtain significance.
- Do not change formulas after seeing regression results without a new author decision.
- Do not allow undocumented variables into regressions, tables, or figures.
- Do not treat validation summaries as causal evidence.
- Do not put proposal-only, pending, not-executed, or unverified variables in the executed dictionary or handoff variable map.
- Do not treat cascade option codes as real dates or quantities without codebook evidence and researcher confirmation.

## human_review_checkpoint
Researcher confirmation is required for every variable formula, source field, unit, level, timing, missing rule, and proxy definition.

## P0_risks
- Key variable formula or source field is unconfirmed.
- Constructed variable lacks validation output or log.
- Variable enters regression without dictionary and audit status.
- Formula is changed without approval.
- Handoff variable map contains `approval_status=pending`, `evidence_class=proposal`, `not_executed`, or `unverified`.
- Questionnaire coding direction, missing semantics, multi-select meaning, or cascade logic is unclear but used for strong-meaning variable construction.

## P1_risks
- Proxy interpretation is uncertain.
- Alternative definitions are documented but require careful downstream wording.
- Missingness or timing may affect sample comparability.

## expected_files
- `output/proposal_variable_dictionary.csv`
- `output/executed_variable_dictionary.csv`
- `handoff_package/variable_map.csv`
- `review/variable_construction_proposal.md`
- `review/variable_construction_audit.md`
- Construction script or do file when execution is approved.
- Construction log when execution is approved.

## evidence_requirements
Variable claims must link to author-approved formulas, source data, construction code, complete logs, validation summaries, and audit status. No log, no claim.

## audit_trail_requirements
Record variable name, approval reference, source fields, construction rule, script, log, validation output, sample effect if any, audit status, and unresolved risks.
