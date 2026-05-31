# Handoff Protocol

This protocol defines how `empirical-regression-agent` delivers final empirical artifacts to a researcher or, after explicit approval, to `empirical-paper-agent`.

## Handoff Boundary

The handoff package may include:

- What was run.
- What was generated.
- What passed audit.
- What failed.
- What remains risky or unresolved.
- Which artifacts support each status claim.

The handoff package must not include manuscript body prose, unsupported causal conclusions, invented interpretations, or claims that unaudited outputs are final.

Audit reports included in the handoff package may verify, classify, and flag artifacts. They must not modify results, change specifications, or convert failed outputs into passed outputs.

## Required Package Structure

A complete handoff package must include at least:

- `tables/`
- `figures/`
- `logs/`
- `do/`
- `variable_map.csv`
- `table_inventory.csv`
- `sample_flow.csv`
- `evidence_map.csv`
- `regression_run_report.md`
- `failed_regressions.md`
- `P0_status.md`
- `P1_risks.md`
- `final_regression_audit.md`
- `handoff_README.md`

Additional project-specific directories may be included when documented.

## Required Inventory Fields

## `variable_map.csv`

Recommended fields:

- `variable_name`
- `label`
- `source_dataset`
- `source_fields`
- `construction_rule`
- `unit`
- `missing_rule`
- `approval_reference`
- `construction_do_file`
- `construction_log`
- `audit_status`

## `table_inventory.csv`

Recommended fields:

- `table_id`
- `table_title`
- `output_path`
- `format`
- `linked_spec_ids`
- `source_do_files`
- `source_logs`
- `audit_status`
- `notes_status`

## `sample_flow.csv`

Recommended fields:

- `step_id`
- `description`
- `input_n`
- `output_n`
- `change_n`
- `approved_rule_reference`
- `source_do_file`
- `source_log`
- `audit_status`

## `evidence_map.csv`

Recommended fields:

- `claim_or_artifact_id`
- `evidence_class`
- `supporting_files`
- `audit_status`
- `risk_level`
- `notes`

## Required Markdown Reports

## `regression_run_report.md`

Must summarize:

- Run date and environment.
- Scripts executed.
- Specs executed.
- Outputs generated.
- Failed or skipped specs.
- Links to logs.

## `failed_regressions.md`

Must list every failed or blocked regression, including:

- `spec_id`
- Script
- Log
- Error or blocker
- Current status
- Required next action

If no regressions failed, the file must explicitly state that no failed regressions were recorded and identify the audit evidence.

## `P0_status.md`

Must list:

- All P0 checks performed.
- Open P0 blockers.
- Resolved P0 blockers.
- Evidence for P0-free status if applicable.

## `P1_risks.md`

Must list substantive cautions, including:

- Mechanism-related evidence limitations.
- Robustness sample shifts.
- Alternative-definition caveats.
- Event-study sparsity or window sensitivity.
- Any author decisions that require careful downstream wording.

## `final_regression_audit.md`

Must state:

- Audit scope.
- Artifacts audited.
- Checks performed.
- Passed outputs.
- Failed or blocked outputs.
- Evidence gaps.
- Final P0/P1/P2 status.

## `handoff_README.md`

Must include:

- Package purpose.
- Directory map.
- Run order.
- Software requirements.
- Reproduction instructions.
- Evidence classification rules.
- Warning that the package is not manuscript prose.
- Whether transfer to `empirical-paper-agent` has been approved.

## Handoff Gate

The package may be marked complete only when:

- Required directories exist.
- Required inventories exist.
- Required Markdown reports exist.
- No open P0 blocker remains.
- P1 risks are disclosed.
- Failed regressions are documented.
- Table and figure inventories map outputs to evidence.
- The researcher has approved any transfer to `empirical-paper-agent`.

## Transfer to Empirical-Paper-Agent

Before transfer, the researcher must confirm:

- The handoff package is final enough for writing use.
- P1 risks are acceptable for downstream drafting.
- `empirical-paper-agent` may use only verified evidence and disclosed author decisions.
- `empirical-paper-agent` must not convert agent inference or open risks into empirical claims.
