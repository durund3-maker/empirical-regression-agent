# Gating Rules

The gate system classifies blockers and risks for empirical execution, audit, export, and handoff.

## P0: Blocking Issues

P0 issues stop execution, finalization, or handoff until resolved. Examples:

- Main regression specification is not confirmed.
- Sample-screening rule is unapproved.
- Merge key or matching rule is unapproved.
- Variable-construction formula is unconfirmed.
- Fixed effects are changed without confirmation.
- Clustering level is changed without confirmation.
- Controls are added, removed, or replaced without confirmation.
- Winsorization, trimming, or outlier handling is unapproved.
- Raw data are modified.
- Core table cannot be traced to spec, do file, log, and output.
- Regression fails but is treated as a successful result.
- Table numbers are manually filled.
- Reviewer or audit process edits numerical results, changes specifications, or converts failed/blocked outputs into passed outputs.
- Failed regressions are not recorded in `failed_regressions.md`.
- A required log is missing or incomplete.
- Handoff package lacks required core artifacts.
- Agent inference is presented as verified evidence.

## P1: Substantive Caution Issues

P1 issues do not automatically block execution, but must be disclosed and reviewed by the researcher. Examples:

- Mechanism-related evidence is weak, proxy-based, or indirect.
- Heterogeneity evidence is at risk of being overstated as mechanism.
- Robustness sample changes materially relative to baseline.
- Alternative variable definitions require careful interpretation.
- Event-study cells are sparse or windows are sensitive.
- Matching quality is mixed but not fatal.
- Some non-core outputs are pending audit.
- Software/package versions differ from the target environment.
- Results depend on author decisions that are documented but contestable.

## P2: Format and Readability Issues

P2 issues concern clarity, navigation, or presentation. They should be fixed when practical but do not block empirical status by themselves. Examples:

- Table titles are verbose but accurate.
- Column labels are readable but not final.
- Notes are complete but not stylistically polished.
- File names are stable but could be clearer.
- Inventory ordering is inconvenient.
- Figure labels need minor formatting.
- Comments in scripts could be clearer.

## Gate Requirements

## Stop Message Contract

Any stop for a P0 blocker, approval gate, manual-review request, handoff transfer gate, final handoff status, or execution beyond approved scope requires a user-facing `Stop Message`. The message must include:

- `why stopped`: the exact gate, blocker, or approval boundary.
- `current status`: what was completed in the current turn and which key files were generated or updated.
- `current problems`: the encountered problems grouped as `P0`, `P1`, `P2`, or non-risk boundaries such as `approval gate` and `manual review`.
- `questions for researcher`: specific questions, confirmations, or choices the researcher must answer, listed in priority order.
- `blocked boundary`: the empirical actions that remain prohibited.
- `required user action`: the concrete decision, correction, approval, or artifact needed.
- `next action after response`: the next workflow step after the researcher replies.
- `project record paths`: generated or updated proposal, gate-status, risk, failure, or handoff records, if any.

Use this fixed user-facing template:

```markdown
## Stop Message

- why stopped: <exact gate, blocker, manual-review request, handoff boundary, or approved-scope boundary>
- current status: <what was completed this turn and which artifacts were generated or updated>
- current problems:
  - P0: <blocking issues, or none>
  - P1: <material disclosed risks, or none>
  - P2: <format/minor issues, or none>
- questions for researcher:
  1. <specific question requiring answer or confirmation>
  2. <specific question requiring answer or confirmation>
- blocked boundary: <what the agent must not do before user response>
- required user action: <specific confirmation, correction, artifact, path, approval, or decision>
- next action after response: <what the agent will do after the user replies>
- project record paths: <relevant proposal/gate/risk/failure/audit/handoff files>
```

Do not rely only on `pipeline_gate_status.md`, `P0_status.md`, `failed_regressions.md`, `needs_author_input`, or `required_next_action` fields. Those records support the stop, but the final response must make the same current problems, researcher questions, and next step visible to the researcher. Do not only say that execution stopped, and do not only cite project files.

If there are no current problems or no researcher questions, write `current problems: none` or `questions for researcher: none` explicitly. P1 and P2 issues do not stop execution by themselves, but when the workflow stops for a P0 blocker, approval gate, manual review, handoff boundary, final handoff status, or approved-scope boundary, the Stop Message must disclose current P1 and P2 risks.

Approval-gate Stop Messages must include concrete answerable questions or confirmation items in `questions for researcher`. A generic request such as "please confirm" is not sufficient.

## Stop Message Language Boundary

When execution stops and the agent provides information for researcher judgment in the conversation, the values in the `Stop Message` should be written in Chinese whenever practical. This applies to the explanation of status, problems, questions, blocked boundaries, required user actions, and next actions.

Keep fixed protocol field names in English for stability. Keep variables, formulas, code, file paths, commands, schema fields, Stata package names, model names, and other technical identifiers in their original form.

This Chinese-language rule does not apply to formal empirical output. Tables, figures, captions, table notes, figure notes, titles, column labels, axis labels, legends, display labels, Appendix Table A, and LaTeX/RTF/XLSX bundles must not be Chinese-localized by this rule.

## Researcher-Judgment Markdown Language

Approval-gate Markdown artifacts written for researcher judgment should use Chinese prose whenever practical. This applies to proposal, decision, gate, and risk-register files such as `review/*proposal*.md`, `review/*decision*.md`, `review/*gate*.md`, and `review/*risk*.md`.

Use Chinese for explanations, approval questions, risk descriptions, recommendation rationales, and next-action instructions. Preserve variables, formulas, field names, code, file paths, commands, Stata package names, model names, schema values, decision enums, and machine-readable blocks in their original form.

This Markdown language rule does not apply to formal empirical tables, figures, captions, table notes, figure notes, titles, labels, legends, Appendix Table A, or LaTeX/RTF/XLSX bundles.

## Intake Gate

Execution may not start until project metadata, data-source inventory, software requirements, and output scope exist or are explicitly marked unavailable.

## Data Gate

Raw data must be read-only. Key checks, data dictionaries, and material provenance must be sufficient to identify open risks before cleaning begins.

## Human Checkpoint Gate

The following require proposal and confirmation before execution:

- Sample rules.
- Merge keys.
- Variable formulas.
- Outlier handling.
- Main specification.
- Fixed effects.
- Clustering.
- Controls.
- Event-study window and omitted period.
- Robustness matrix.
- Heterogeneity or mechanism-related design.
- Final table order.
- Transfer to `empirical-paper-agent`.

Regression proposals must include a Fixed Effects Decision Node. The node must document `TWFE vs mixed regression`, including candidate fixed effects, candidate mixed controls, selected FE strategy, rejected FE strategy, and rejection reason. Direct no-FE proposals are P0 unless they document one of three technical exceptions: no usable FE dimension exists, fixed effects are fully collinear with key variables, or sample sparsity/degrees-of-freedom constraints make FE models non-estimable.

## Execution Gate

A task is not complete unless the corresponding executable file ran successfully, produced a log, and wrote expected artifacts or a failure record.

## Output Gate

Tables and figures cannot be final unless each output has:

- Stable path.
- Source script.
- Source log.
- Linked specification or generation command.
- Audit status.

## Audit Gate

Empirical results are verified only when audit status is `passed`. If status is `failed`, `blocked`, or `needs_author_input`, the output may be listed but not treated as final evidence.

Auditors may inspect, compare, classify, and report. They must not change sample rules, variables, fixed effects, clustering, controls, numerical results, significance markers, or output status except through documented audit-status records.

## Handoff Gate

Handoff is blocked by any open P0 issue. P1 issues must be summarized in `P1_risks.md`. P2 issues may be listed as formatting notes.
