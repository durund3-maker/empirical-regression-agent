---
name: pre-regression-proposal
description: Generate a pre-execution analysis proposal before cleaning, regression, Stata execution, or pilot results package work. Use this skill to turn variable dictionaries, causal-chain maps, table plans, and P0/P1 risks into one recommended plan, alternatives, decision sheet, and execution gate for researcher approval; it must not read raw data or execute analysis.
---

# pre-regression-proposal

## name
pre-regression-proposal

## description
Use this skill after project intake, causal-chain mapping, and pilot analysis planning, but before any cleaning, regression, Stata execution, descriptive-results package, or pilot-results package. It converts derived planning artifacts into a pre-execution proposal package: one recommended main plan, three alternative plans, one rejected full-causal-chain plan, a researcher decision sheet, a risk register, and a revised pilot table plan. It must not read raw data, execute analysis, generate empirical results, write manuscript prose, or clear execution gates without explicit researcher approval.

## when_to_use
Use when a project has planning artifacts such as a draft variable dictionary, causal-chain variable map, pilot table plan, claim-boundary memo, and P0/P1 risk records, and the user wants a compact approval package instead of manually filling a detailed researcher confirmation form item by item.

This skill is appropriate immediately before a pilot results package or pre-regression execution package is requested. It is not a replacement for human-in-the-loop approval; it reorganizes approvals into a proposal and decision workflow.

## required_inputs
- `output/variable_dictionary_draft.csv`
- `output/causal_chain_variable_map.csv`
- `output/table_plan_pilot.csv`
- `review/identification_feasibility_report.md`
- `review/causal_claim_boundary.md`
- `review/P0_status.md`
- `review/P1_risks.md`

Optional inputs:

- `review/project_intake_report.md`
- `review/pilot_analysis_plan.md`
- `review/pilot_execution_gate.md`
- `review/researcher_confirmation_form.md`

If optional inputs are missing, do not fail. Mark them as `missing optional input` in the proposal audit trail and proceed from the required artifacts only.

## required_outputs
- `review/pre_execution_analysis_proposal.md`
- `review/pre_execution_decision_sheet.md`
- `review/pre_execution_risk_register.md`
- `output/table_plan_pilot_revised.csv`
- `output/plans/01_identification_strategy_summary.md`
- `output/plans/02_pre_execution_analysis_plan.md`
- `output/plans/03_data_processing_rules.md`
- `output/plans/04_variable_construction_plan.md`
- `output/plans/05_sample_rules.md`
- `output/plans/06_estimator_and_se_plan.md`
- `output/plans/07_table_figure_plan.md`
- `output/plans/08_risk_and_downgrade_statement.md`
- `review/hitl/pre_execution_approval_checklist.md`
- `review/hitl/HITL_REVIEW_INDEX_pre_execution.md`

These outputs are a proposal package, not a results package.

## output_language
Researcher-facing Markdown prose in the proposal, decision sheet, and risk register should be written in Chinese whenever practical. Preserve variables, formulas, field names, code, file paths, commands, Stata package names, model names, schema values, status enums, decision enums such as `APPROVE_MAIN_PLAN`, and machine-readable blocks in their original form.

## workflow
1. Load only derived planning artifacts.
   - Read only the variable dictionary, causal-chain map, table plan, claim-boundary memo, P0/P1 risk reports, and optional planning/researcher-confirmation artifacts.
   - Do not read raw data.
   - Do not read Excel, dta, or csv files that are raw data.
   - Do not run statistical code, Stata, Python analysis scripts, R scripts, or model commands.
2. Identify strongest and weakest chain nodes.
   - Summarize which chain nodes have the strongest variable coverage.
   - Summarize which nodes have the weakest variable coverage.
   - Identify nodes that can only be descriptive.
   - Identify nodes that cannot enter regression.
   - Identify nodes requiring external data before causal or objective claims.
3. Generate Recommended Main Plan.
   - Include plan name.
   - Include research question for the pilot stage.
   - Include usable chain segment.
   - Identify primary X / M / Y.
   - Identify candidate controls.
   - Propose index construction, if justified by mapped variables and subject to approval.
   - List variables to use only descriptively.
   - List variables excluded from regression.
   - List expected tables.
   - List expected figures.
   - State allowed claim type.
   - State forbidden claim type.
   - State execution prerequisites.
   - Flag P0/P1 risks.
   - The recommended main plan should fit current data quality and variable coverage. If the strongest current chain is C -> D -> E -> F, recommend that middle segment rather than a complete A -> G causal chain.
4. Generate Alternative Plan 1: Conservative Descriptive Plan.
   - Include sample profile.
   - Include frequencies.
   - Include cross-tabs.
   - Include mean comparisons.
   - Do not include regression.
   - Do not include a mechanism chain.
   - Allowed claim type is only `descriptive pattern`.
5. Generate Alternative Plan 2: Exploratory Association Plan.
   - Allow correlational regressions only if researcher approval is explicit.
   - Candidate tools may include OLS, logit, ordered logit, or simple index comparisons.
   - Allowed claim types are only `association` and `suggestive pilot evidence`.
   - Forbid `causal effect`.
   - State that if variable direction, coding, scale direction, multi-select coding, or missing-value handling is unclear, regression remains P0-blocked.
6. Generate Alternative Plan 3: Mechanism-Chain Exploratory Plan.
   - Explore only better-covered middle-chain segments such as C -> D -> E -> F.
   - Treat A/B/G nodes only as background, descriptive modules, or P1 cautions unless external data and approvals exist.
   - Do not claim the complete chain.
   - Do not claim that mediation is formally identified.
   - State that heterogeneity is not mechanism unless the researcher explicitly defines and documents it as such.
7. Generate Rejected Plan: Full Causal Chain Plan.
   - Explain why the current pilot cannot prove the full A -> G causal chain.
   - List missing external data.
   - List forbidden conclusions.
   - Identify evidence that can only motivate future research.
8. Generate Decision Sheet.
   - The researcher must choose exactly one of:
     - `APPROVE_MAIN_PLAN`
     - `APPROVE_ALT_1`
     - `APPROVE_ALT_2`
     - `APPROVE_ALT_3`
     - `REVISE_AND_RESUBMIT`
     - `STOP`
   - Allow natural-language notes for allowed modifications, variables to drop, index construction changes, exploratory association permission, whether A/B/G should be excluded from regression, and claim-language restrictions.
   - Default status is `NOT_APPROVED`.
   - Without a checked option or clear natural-language approval, Regression execution P0 remains open.
9. Generate Risk Register.
   - List P0 risks that block execution.
   - List P1 risks that allow cautious pilot execution.
   - List variables needing author confirmation.
   - List coding decisions needing author confirmation.
   - List causal claims forbidden before external data.
   - List data limitations.
   - List next data-collection needs.
10. Update revised table plan.
   - Write `output/table_plan_pilot_revised.csv`.
   - Preserve the original `table_plan_pilot.csv` fields.
   - Add:
     - `recommended_plan`
     - `plan_option`
     - `execution_status`
     - `claim_boundary`
     - `P0_gate`
     - `P1_risk`
     - `researcher_approval_required`
   - Do not delete important information from the original table plan.
11. Generate HITL review access package.
   - Write Markdown versions of every critical pre-execution review file under `output/plans/` and `review/hitl/`.
   - Write `review/hitl/HITL_REVIEW_INDEX_pre_execution.md` with the current gate name, workflow status, approved items, unapproved items, file list, Markdown links, full relative `Path:` entries, file purpose, researcher check focus, and copyable `APPROVE`, `REVISE`, and `REJECT` reply templates.
   - The index must be sufficient even when links are not clickable: every item needs a full relative path, short description, and approval decision needed.

## proposal_structure
`review/pre_execution_analysis_proposal.md` must contain:

1. Executive summary
2. Recommended main plan
3. Alternative Plan 1: Conservative descriptive plan
4. Alternative Plan 2: Exploratory association plan
5. Alternative Plan 3: Mechanism-chain exploratory plan
6. Rejected Plan: Full causal chain plan
7. Variable role summary
8. Table and figure plan
9. Coding and index construction proposal
10. Claim boundary
11. P0/P1 risk summary
12. What the researcher must approve

## decision_sheet_rules
`review/pre_execution_decision_sheet.md` must contain this editable decision block:

```markdown
Decision:
- [ ] APPROVE_MAIN_PLAN
- [ ] APPROVE_ALT_1
- [ ] APPROVE_ALT_2
- [ ] APPROVE_ALT_3
- [ ] REVISE_AND_RESUBMIT
- [ ] STOP

Researcher modifications:
- Selected plan:
- Variables to drop:
- Variables to use only descriptively:
- Index construction approved: YES / NO / REVISE
- Exploratory association approved: YES / NO / REVISE
- A/B/G regression allowed: YES / NO / REVISE
- Claim language restrictions:
- Additional notes:
```

Rules:

- If nothing is checked and no natural-language approval is provided, Regression execution P0 cannot be cleared.
- Default status is `NOT_APPROVED`.
- The agent must not treat silence as approval.
- The agent must not infer approval from the existence of the proposal.
- A generalized approval such as "approve all", "全部批准", or "yes to all" cannot clear high-risk items listed under `high_risk_itemized_approval_rules`.
- If the researcher selects `REVISE_AND_RESUBMIT`, revise the proposal package only; do not execute analysis.
- If the researcher selects `STOP`, do not execute analysis and record the stop decision.

## high_risk_itemized_approval_rules
The proposal and decision sheet must contain separate confirmation items for these operations:

- Weak-identification data entering any regression.
- Small-N or over-parameterized model execution.
- Cross-sectional questionnaire data being described with any causal-inference language.
- Index construction direction, including reverse coding.
- Likert scale direction.
- Multi-select question missingness or unchecked-option meaning.
- Cascade question codes being used as real time or quantity variables.
- Inclusion of any hard-gated or fragile regression table in the main bundle.
- Handoff transfer to `empirical-paper-agent`.

Each item must state what will be done, why it is high risk, the downgrade boundary, the only allowed claim wording if execution continues, and whether main-bundle inclusion is allowed.

## forbidden_actions
- Do not execute regressions.
- Do not run Stata.
- Do not read raw data.
- Do not clean data.
- Do not generate result tables.
- Do not generate statistical conclusions.
- Do not write manuscript body text.
- Do not describe the pilot as formal causal identification.
- Do not describe association as causality.
- Do not describe self-reported mechanism as verified mechanism.
- Do not treat researcher silence as approval.
- Do not choose the final plan on behalf of the researcher.
- Do not overwrite `researcher_confirmation_form.md`.
- Do not delete `P0_status.md`.
- Do not clear Formal causal identification P0.

## human_review_checkpoint
Before a researcher explicitly approves a plan, Regression execution P0 cannot be cleared.

Approval can be documented in either of these ways:

- The researcher edits or approves `review/pre_execution_decision_sheet.md` with a selected option.
- The researcher states clearly in conversation, for example: "Use plan X, allow exploratory association, exclude A/B/G from regression, and keep causal language prohibited."

Even if the researcher approves pilot execution, Formal causal identification P0 remains open unless a separate, documented formal identification design with necessary data is approved.

If the researcher selects `REVISE_AND_RESUBMIT`, the agent may only revise the proposal package. It must not clean data, run scripts, run regressions, generate tables, or write results.

## P0_risks
- Missing variable dictionary.
- Missing causal-chain map.
- Missing claim boundary.
- No approved plan.
- Ambiguous variable roles.
- Ambiguous scale direction.
- Ambiguous multi-select coding.
- Missing table plan.
- Attempt to execute regression before approval.
- Attempt to use pilot evidence as formal causal identification.
- Attempt to clear Regression execution P0 without explicit researcher approval.
- Attempt to clear Formal causal identification P0 through this skill.
- Attempt to clear high-risk itemized approval with generalized approval language.

## P1_risks
- Subjective perception variables.
- Common method bias.
- Retrospective self-reporting.
- Selection into pilot sample.
- Weak A/B/G node coverage.
- Weak objective street outcome measurement.
- Index construction sensitivity.
- Small pilot sample size.
- Exploratory multiple testing risk.
- Claim-language drift from association to causality.

## expected_files
- `review/pre_execution_analysis_proposal.md`
- `review/pre_execution_decision_sheet.md`
- `review/pre_execution_risk_register.md`
- `output/table_plan_pilot_revised.csv`
- `output/plans/01_identification_strategy_summary.md`
- `output/plans/02_pre_execution_analysis_plan.md`
- `output/plans/03_data_processing_rules.md`
- `output/plans/04_variable_construction_plan.md`
- `output/plans/05_sample_rules.md`
- `output/plans/06_estimator_and_se_plan.md`
- `output/plans/07_table_figure_plan.md`
- `output/plans/08_risk_and_downgrade_statement.md`
- `review/hitl/pre_execution_approval_checklist.md`
- `review/hitl/HITL_REVIEW_INDEX_pre_execution.md`

## evidence_requirements
- All variable roles must come from `output/variable_dictionary_draft.csv` and `output/causal_chain_variable_map.csv`.
- All claim boundaries must come from `review/causal_claim_boundary.md`.
- All risks must come from `review/P0_status.md`, `review/P1_risks.md`, and `review/identification_feasibility_report.md`.
- Do not use raw data.
- Do not use result tables.
- Do not add unmapped variable roles by intuition.
- If a required artifact is missing, mark the proposal blocked rather than filling the gap by inference.

## audit_trail_requirements
Record:

- Which inputs were used.
- Which optional inputs were missing.
- Plan generation date.
- P0 risks retained.
- P1 risks retained.
- Whether approval has been given.
- Execution status, which is `NOT_APPROVED` by default.
- Any researcher decision reference used to change status.

## relationship_to_existing_confirmation_form
This skill replaces the inefficient workflow of manually filling `researcher_confirmation_form.md` item by item. It does not remove researcher approval.

The detailed `researcher_confirmation_form.md` can remain as an optional appendix or diagnostic checklist. The new default workflow is:

1. Proposal package.
2. Decision sheet approval.
3. Execution plan finalization.
4. Pilot results package.

If the proposal and confirmation form conflict, the latest explicit researcher approval controls. Silence, ambiguity, or the mere presence of generated files is not approval.

## examples_of_researcher_decisions
Acceptable decision examples:

1. "Use Recommended Main Plan; allow C/D/E/F indexes; allow exploratory association; A/B/G descriptive only; all claims limited to suggestive pilot evidence."
2. "Use Conservative Descriptive Plan; no regression; only frequencies, cross-tabs, and mean comparisons."
3. "REVISE_AND_RESUBMIT: remove all G-node analysis; F descriptive only; no index construction."

## completion_criteria
The skill is complete only when:

- All required inputs are present or missing inputs are marked as P0 blockers.
- Optional inputs are either used or marked as missing optional inputs.
- `review/pre_execution_analysis_proposal.md` exists and follows `proposal_structure`.
- `review/pre_execution_decision_sheet.md` exists and defaults to `NOT_APPROVED`.
- `review/pre_execution_risk_register.md` exists and separates P0 and P1 risks.
- `output/table_plan_pilot_revised.csv` exists and preserves original table-plan fields plus required new fields.
- The HITL review index exists, uses Markdown links plus full relative `Path:` entries, and lists approval/revision/rejection templates.
- All critical pre-execution approval materials have Markdown versions for quick human review.
- The proposal clearly states that Regression execution P0 remains open until researcher approval.
- The proposal clearly states that Formal causal identification P0 cannot be cleared by this skill.
- No raw data were read and no analysis was executed.
