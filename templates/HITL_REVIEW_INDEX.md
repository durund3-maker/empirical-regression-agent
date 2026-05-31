# HITL Review Index

## Gate

- Current gate: `<gate_name>`
- Workflow status: `<workflow_status>`

## Approval Status

### Approved Items

- `<approved_item>`

### Not Yet Approved

- `<unapproved_item>`

## Review Files

- [Pre-execution analysis plan](../output/plans/02_pre_execution_analysis_plan.md)  
  Path: `projects/<project_id>/output/plans/02_pre_execution_analysis_plan.md`  
  Absolute Path: `<project_root_absolute_path>/output/plans/02_pre_execution_analysis_plan.md`  
  Purpose: Review data processing rules, variable formulas, sample rules, controls, estimator, standard errors, and table plan.  
  Check: Confirm whether the proposed analysis stays inside the approved identification boundary and whether any P0/P1 risks need revision.  
  Decision needed: `APPROVE` / `REVISE` / `REJECT`

- [Approval checklist](pre_execution_approval_checklist.md)  
  Path: `projects/<project_id>/review/hitl/pre_execution_approval_checklist.md`  
  Absolute Path: `<project_root_absolute_path>/review/hitl/pre_execution_approval_checklist.md`  
  Purpose: Record itemized approval decisions for the current HITL gate.  
  Check: Every required item has a clear decision; high-risk items are approved separately when applicable.  
  Decision needed: Complete the checklist or respond in conversation using one of the templates below.

## Reply Templates

### Approve

```text
APPROVE:
- Gate: <gate_name>
- Approved files:
  - projects/<project_id>/output/plans/02_pre_execution_analysis_plan.md
  - projects/<project_id>/review/hitl/pre_execution_approval_checklist.md
- High-risk itemized approvals: <list item IDs or write none>
- Notes: <optional>
```

### Revise

```text
REVISE:
- Gate: <gate_name>
- File and section to revise: <path + section>
- Requested change: <specific change>
- Items still blocked: <list>
```

### Reject

```text
REJECT:
- Gate: <gate_name>
- Rejected item: <specific rule/spec/table plan>
- Reason: <brief reason>
- Next preferred action: <stop or revise>
```
