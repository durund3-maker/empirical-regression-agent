# Pre-Execution Analysis Proposal

## Required Markdown Review Package

At `Pre-Execution Analysis Approval Gate`, generate these Markdown files for researcher review before any execution:

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

The HITL review index must list each file with both a Markdown link and a full relative `Path:` entry, plus purpose, focus checks, and approval decision needed.

## High-Risk Itemized Approvals

Generalized approval such as "approve all" or "全部批准" does not clear the following items. Each item needs a separate decision when applicable.

| Item | Planned action | Why high risk | Downgrade boundary | Allowed wording if continued | Main bundle allowed |
|---|---|---|---|---|---|
| Weak identification enters regression |  |  |  |  | YES / NO / REVISE |
| Small-N or over-parameterized model |  |  |  |  | YES / NO / REVISE |
| Cross-sectional questionnaire causal language |  |  |  |  | YES / NO / REVISE |
| Index direction |  |  |  |  | YES / NO / REVISE |
| Likert direction |  |  |  |  | YES / NO / REVISE |
| Multi-select missingness |  |  |  |  | YES / NO / REVISE |
| Cascade code timing or quantity use |  |  |  |  | YES / NO / REVISE |
| Fragile table main-bundle inclusion |  |  |  |  | YES / NO / REVISE |
| Transfer to empirical-paper-agent |  |  |  |  | YES / NO / REVISE |

## Decision

- [ ] APPROVE_LOW_RISK_ONLY
- [ ] APPROVE_ITEMIZED_HIGH_RISK_AS_MARKED
- [ ] REVISE_AND_RESUBMIT
- [ ] STOP
