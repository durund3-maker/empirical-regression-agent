---
name: hitl-review
description: Generate centralized human-in-the-loop review indexes for empirical approval gates with Markdown links, full relative paths, file purposes, review focus, and approval/revise/reject templates.
---

# hitl-review

## when_to_use
Use at every HITL approval gate, including Identification Strategy Gate, Data Processing Gate, Pre-Execution Analysis Approval Gate, Baseline Regression Gate, Robustness Matrix Gate, table-order approval, handoff transfer approval, and any manual-review stop.

## required_outputs
- A centralized review index: default `review/HITL_REVIEW_INDEX.md`, or stage-specific `review/hitl/HITL_REVIEW_INDEX_<stage>.md`.
- Markdown versions of all critical approval materials. At pre-execution this includes:
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

## index_required_content
The index must include:

1. Current gate name.
2. Current workflow status.
3. Approved items.
4. Unapproved items.
5. Files the researcher must review this round.
6. Markdown link for each file.
7. Full relative path for each file in a `Path:` line.
8. Purpose of each file.
9. Key questions or checks for the researcher.
10. Approval decision needed for each file.
11. Copyable `APPROVE`, `REVISE`, and `REJECT` reply templates.

## link_format
Use both Markdown links and full relative paths:

```md
- [Pre-execution analysis plan](../output/plans/02_pre_execution_analysis_plan.md)  
  Path: `projects/<project_id>/output/plans/02_pre_execution_analysis_plan.md`  
  Purpose: Review data processing rules, variable formulas, sample rules, controls, estimator, standard errors, and table plan.  
  Decision needed: `APPROVE` / `REVISE` / `REJECT`
```

Do not rely on Codex or IDE link rendering. If a link is not clickable, the `Path:` line must still let the researcher locate the file.

## final_reply_rule
When stopping at a HITL gate, the final reply must list the review index first and then key review files. Each entry must include a Markdown link, full relative path, short description, and approval decision needed. Do not write only "please review the files" or "see output folder".

For `Pre-Execution Analysis Approval Gate`, start with:

```md
Workflow paused at: Pre-Execution Analysis Approval Gate

Please review the following index first:

- [HITL Review Index](projects/<project_id>/review/hitl/HITL_REVIEW_INDEX_pre_execution.md)  
  Path: `projects/<project_id>/review/hitl/HITL_REVIEW_INDEX_pre_execution.md`
```

## forbidden_actions
- Do not proceed past a HITL gate without a centralized index.
- Do not provide only `.csv`, `.xlsx`, `.tex`, or `.pdf` approval materials when a Markdown review version is required.
- Do not omit full relative paths from the index or final gate response.
