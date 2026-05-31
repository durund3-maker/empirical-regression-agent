# Empirical Regression Subagents

These subagents divide the empirical-regression workflow into preparation, estimation, table, audit, and handoff responsibilities. They operate under `AGENTS.md`, `WORKFLOW.md`, `agent_core/`, `config/`, and `skills/`.

## Subagent Uses

| Subagent | Purpose |
| --- | --- |
| `dataprep-agent` | Intake materials, audit data inventory, propose cleaning, and define variables while keeping raw data read-only. |
| `estimator-agent` | Audit and execute approved regression specifications, event studies, robustness checks, and heterogeneity or mechanism-related models. |
| `table-agent` | Generate descriptive outputs and audit empirical tables or figures for traceability and numerical integrity. |
| `reviewer-agent` | Perform read-only cross-artifact audit and report P0/P1/P2 risks under `review/`. |
| `handoff-agent` | Assemble audited artifacts into a handoff package without manuscript prose or result interpretation. |

## Recommended Calling Order

1. `dataprep-agent`
2. `estimator-agent`
3. `table-agent`
4. `reviewer-agent`
5. `handoff-agent`

The workflow may loop back after review findings. For example, a P0 spec issue from `reviewer-agent` returns to `estimator-agent` only after researcher confirmation.

## Skill Mapping

| Subagent | Related skills |
| --- | --- |
| `dataprep-agent` | `project-intake`, `data-inventory-audit`, `data-cleaning`, `variable-construction` |
| `estimator-agent` | `regression-spec-audit`, `baseline-regression`, `event-study`, `robustness-checks`, `heterogeneity-mechanism` |
| `table-agent` | `descriptive-statistics`, `table-output-audit` |
| `reviewer-agent` | `regression-spec-audit`, `table-output-audit`, `handoff-package-builder`, plus read-only inspection of all skill outputs |
| `handoff-agent` | `handoff-package-builder` |

## Code Generation Permissions

Can generate code or script scaffolds only when approvals are documented:

- `dataprep-agent`: cleaning and variable-construction scaffolds.
- `estimator-agent`: approved regression workflow scaffolds.
- `table-agent`: approved descriptive-statistics or table-export workflows.

Cannot generate code:

- `reviewer-agent`, except review reports under `review/`.
- `handoff-agent`, except handoff package manifests and README files.

## Regression Execution Permissions

Can execute approved regressions:

- `estimator-agent` only.

Cannot execute regressions:

- `dataprep-agent`
- `table-agent`
- `reviewer-agent`
- `handoff-agent`

## Read-Only Audit Subagents

- `reviewer-agent` is read-only with respect to data, code, configs, tables, figures, logs, and handoff artifacts. It may write audit reports only under `review/`.
- `table-agent` is audit-only for generated regression tables and figures, but may generate descriptive outputs from approved data.

## HITL Requirements

Researcher confirmation is required for:

- Sample-screening rules.
- Merge keys and matching rules.
- Variable-construction formulas.
- Winsorization, trimming, and outlier handling.
- Main regression specification.
- Fixed effects.
- Clustering level.
- Controls.
- Event-study window and omitted period.
- Robustness matrix.
- Heterogeneity, mechanism-related, moderation, or mediation design.
- Final table order.
- Handoff completion and transfer to `empirical-paper-agent`.

## P0 Escalation Conditions

Escalate to P0 when:

- Raw data are modified.
- A required approval is missing for sample, merge, variable, FE, cluster, controls, estimator, event-study, robustness, or mechanism-related design.
- Required logs are missing or incomplete.
- Failed regressions are not recorded.
- Table values are manually entered or edited.
- Core output cannot be traced to spec, script, log, and output.
- Agent inference is presented as verified evidence.
- Handoff package lacks required core artifacts.
- Any subagent writes manuscript body prose or unsupported causal conclusions.

## Boundary With Empirical-Paper-Agent

These subagents produce empirical artifacts, audit records, risk disclosures, and handoff packages. They do not write manuscript body text, convert heterogeneity into mechanism claims, decide identification validity, or translate empirical outputs into paper conclusions.

Transfer to `empirical-paper-agent` requires explicit researcher approval. The receiving agent may use only verified evidence and disclosed author decisions, and must not convert agent inference or open risks into empirical claims.
