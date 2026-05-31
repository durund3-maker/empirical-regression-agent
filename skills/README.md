# Empirical Regression Agent Skills

These skills operationalize the reusable workflow for `empirical-regression-agent`. They produce empirical artifacts, audits, and handoff packages only. They do not write manuscript prose, invent empirical content, or convert unaudited outputs into evidence.

## Skill Uses

| Skill | Purpose |
| --- | --- |
| `pipeline-orchestrator` | Total-control skill used at project start to run the workflow to the next approval gate. It coordinates the other skills, reduces manual confirmations, preserves researcher approval, and cannot clear formal causal identification P0. |
| `project-intake` | Read project metadata, inventory project folders, and create first material, variable, table, and missing-information maps. |
| `identification-proposal` | Propose candidate Y/X/unit/time/proxy variables and feasible identification strategies before regression execution. |
| `data-inventory-audit` | Audit raw data availability, paths, formats, keys, time variables, sample period, Git exposure, and safety risks. |
| `data-cleaning` | Draft cleaning proposals, sample-flow records, decision logs, and approved cleaning-script scaffolds. |
| `variable-construction` | Define and audit variable formulas, source fields, units, timing, levels, and validation checks. |
| `descriptive-statistics` | Generate traceable descriptive statistics, sample distributions, group comparisons, balance, or SMD outputs. |
| `pre-regression-proposal` | Turn variable dictionaries, causal-chain maps, pilot table plans, and P0/P1 risks into a pre-execution proposal package and decision sheet for researcher approval before any pilot results package or regression execution. |
| `hitl-review` | Generate centralized HITL review indexes with Markdown links, full relative paths, file purposes, and approval/revise/reject templates. |
| `regression-spec-audit` | Check `regression_specs.yml` completeness before any regression execution. |
| `stata-execution-runner` | Execute approved Stata do files through stata-mcp or local Stata batch mode, verify esttab/estout, capture logs, and prevent Python/R substitution for official Stata results. |
| `baseline-regression` | Execute approved main regressions and export logged baseline tables. |
| `event-study` | Execute approved dynamic-effect and pre-trend workflows with event-window and omitted-period audit. |
| `robustness-checks` | Execute approved robustness checks from `robustness_matrix.yml`. |
| `heterogeneity-mechanism` | Execute and audit approved heterogeneity, mechanism-related, moderation, or mediation designs while preserving evidence-class boundaries. |
| `table-output-audit` | Audit generated tables for traceability, notes, labels, numbers, stars, FE, clustering, controls, and blank rows. |
| `tables-figures-appendix-builder` | Build one standalone XeLaTeX Tables and Figures plus Appendix file from audited official tables and figures, excluding cross-check artifacts by default and requiring notes for every artifact. |
| `tables-figures-format` | Audit Tables/Figures layout before PDF build, final status, or handoff main-bundle inclusion. |
| `appendix-latex-builder` | Build an appendix-only XeLaTeX file when the researcher explicitly requests Appendix-only or validation-appendix delivery. |
| `handoff-package-builder` | Assemble the audited empirical handoff package for researcher review or approved transfer. |

## Recommended Calling Order

Default project-start path:

1. `pipeline-orchestrator` in `PLAN_AUTOPILOT` mode.
2. Researcher approval of identification and data-processing gates.
3. `pipeline-orchestrator` in `EXECUTION_AUTOPILOT` mode.

Detailed debugging or high-risk path:

1. `project-intake`
2. `data-inventory-audit`
3. `identification-proposal`
4. `data-cleaning`
5. `variable-construction`
6. `descriptive-statistics`
7. `pre-regression-proposal`
8. `hitl-review` at each approval stop
9. `regression-spec-audit`
10. `stata-execution-runner` when Stata is the main project language and official execution is approved
11. `baseline-regression`
12. `event-study`
13. `robustness-checks`
14. `heterogeneity-mechanism`
15. `table-output-audit`
16. `tables-figures-appendix-builder` when manuscript-ready table/figure delivery is requested
17. `tables-figures-format` before PDF/final/handoff status
18. `appendix-latex-builder` only when appendix-only delivery is explicitly requested
19. `handoff-package-builder`

## Human-In-The-Loop Skills

All skills may surface human-review needs. The following require confirmation before execution or finalization when the relevant choice is not already documented:

- `pipeline-orchestrator`: recommended or alternative plan approval, `REVISE_AND_RESUBMIT`, raw-data safety failure, unresolved PII/open-text leakage risk, execution beyond approved scope, formal causal identification claim, explicit manual-review request, and final handoff completion.
- `project-intake`: project scope, owner, confidentiality constraints, expected outputs.
- `identification-proposal`: selected identification strategy, treatment assignment rule, proxy variables, control-group concept, event-window concept, and causal-language boundary.
- `data-inventory-audit`: ambiguous provenance, authorization, safety, keys, and file roles.
- `data-cleaning`: sample rules, merge keys, deduplication, recodes, missing rules, outlier handling.
- `variable-construction`: formulas, source fields, units, timing, levels, missing rules.
- `descriptive-statistics`: grouping variables, balance design, SMD definitions, final table order.
- `pre-regression-proposal`: recommended plan, alternatives, table plan revisions, exploratory association permission, index construction rules, and claim-language restrictions.
- `hitl-review`: centralized review index accessibility, Markdown review versions, and final response file list at every approval gate.
- `regression-spec-audit`: specification, FE, clustering, controls, sample, estimator, expected table.
- `stata-execution-runner`: Stata path or MCP endpoint, `esttab` / `estout` installation or fallback, and handling of Stata execution failures.
- `baseline-regression`: approved main spec and handling of failures or unexpected samples.
- `event-study`: window, omitted period, binning, lead/lag construction, output order.
- `robustness-checks`: robustness matrix and all baseline deviations.
- `heterogeneity-mechanism`: subgroup, mechanism-related, moderation, or mediation design and evidence labels.
- `table-output-audit`: final table order and acceptance of disclosed P1 risks.
- `tables-figures-appendix-builder`: final table/figure order, `Tables and Figures` versus `Appendix` placement rationale, output path, and acceptance of validation appendix labeling if cross-check artifacts are explicitly requested.
- `tables-figures-format`: note centering, decimal precision, main-table page breaks, Appendix placement, duplicate table-number prevention, placeholders, and PDF compilation readiness.
- `appendix-latex-builder`: Appendix-only inclusion scope, final table/figure order, output path, and acceptance of validation appendix labeling if cross-check artifacts are explicitly requested.
- `handoff-package-builder`: final handoff status and any transfer to `empirical-paper-agent`.

## Read-Only Skills

- `project-intake` reads and maps materials but writes only inventory and review outputs.
- `data-inventory-audit` is read-only with respect to data and only reports.
- `pre-regression-proposal` reads only derived planning artifacts and writes a proposal package; it must not read raw data, execute analysis, or clear execution gates.
- `regression-spec-audit` audits specs and does not execute regressions.
- `table-output-audit` audits exported tables and must not edit numerical results.
- `tables-figures-appendix-builder` and `appendix-latex-builder` assemble audited outputs only and must not write manuscript body text.
- `stata-execution-runner` executes only approved do files. It does not choose specifications, construct variables, or write manuscript claims.

## Skills That Can Generate Code

- `data-cleaning` can generate cleaning-script scaffolds after documenting required approvals.
- `variable-construction` can generate construction workflows after formulas are approved.
- `descriptive-statistics` can generate descriptive-statistics scripts.
- `baseline-regression`, `event-study`, `robustness-checks`, and `heterogeneity-mechanism` can generate execution scripts from approved specs or matrices.

## Skills That Can Execute Regressions

- `baseline-regression`
- `event-study`
- `robustness-checks`
- `heterogeneity-mechanism`

For Stata-primary projects, these skills must route official execution through `stata-execution-runner`. They must record logs, explicit FE and clustering, source specs, exported outputs, and failure handling. No log, no claim.

## Audit-Only Skills

- `data-inventory-audit`
- `pre-regression-proposal`
- `regression-spec-audit`
- `table-output-audit`

Other skills also produce audit records, but these audit-only skills are primarily used to inspect readiness, risks, and boundaries rather than execute empirical models.

`pre-regression-proposal` is used after pilot analysis planning and before a pilot results package or regression execution. It replaces the inefficient workflow of manually filling a detailed confirmation form item by item by generating a recommended plan, alternatives, risk register, revised table plan, and editable decision sheet. It does not abolish human review: before explicit researcher approval, Regression execution P0 remains open. It also cannot clear Formal causal identification P0; that requires a separate approved identification design and supporting evidence.

`pipeline-orchestrator` is the preferred project-start skill. It is a coordinator rather than a replacement for the specialized skills. It should automatically advance low-risk steps, record P1 risks without stopping, and stop only for P0 blockers or required researcher gates. It reduces the number of manual confirmations, but it cannot cancel researcher approval, treat silence as approval, execute beyond approved scope, or clear formal causal identification P0.

## Handoff Package Skill

- `handoff-package-builder` creates `handoff_package/` and its manifest, README, evidence files, failure records, and audit report. It does not write manuscript prose or transfer materials to `empirical-paper-agent` without explicit researcher confirmation.

## Future Scripts and Templates

This stage defines skill instructions only. Future implementation can add deterministic helpers when repeated execution makes them useful:

- Stata runner wrapper: execute approved do files through `stata-mcp` when configured or local Stata batch mode as fallback, capture return codes, verify `esttab` / `estout`, and write run metadata.
- Data safety checker: scan inventories for raw-data Git exposure, sensitive paths, and authorization flags.
- Log parser: extract Stata errors, return codes, sample counts, merge diagnostics, and output paths.
- Table inventory generator: map table files to specs, logs, formats, notes, and audit status.
- Tables and Figures plus Appendix builder: assemble official audited evidence into a single manuscript-ready empirical artifact with placement rationale and required notes.
- Handoff manifest builder: generate `file_manifest.csv` and check required package contents.

These helpers should live under future `scripts/` or `templates/` directories and must not duplicate project-specific variables, results, or external repository code.

## Future Subagent Boundaries

Later subagents should separate execution from audit where risk is high:

- Data safety auditor for raw-data and confidentiality checks.
- Stata execution runner for approved scripts only; Python/R results are validation or cross-check artifacts unless explicitly approved otherwise.
- Regression spec auditor for P0 readiness checks.
- Table output auditor for traceability and no-manual-number checks.
- Tables and Figures plus Appendix builder for manuscript-ready empirical artifacts without body prose.
- Handoff auditor for final P0/P1/P2 package status.

## Shared Rules

All skills must follow no invention, raw data read-only, no log/no claim, P0/P1/P2 gating, audit-trail recording, and evidence classification. Table numbers must come from Stata or another approved executable output, never manual entry. Heterogeneity is not mechanism unless explicitly defined and documented by the researcher.
