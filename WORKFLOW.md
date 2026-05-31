# Workflow

This workflow governs concrete empirical projects built from this framework. Each stage produces executable artifacts, audit records, or proposals. It does not produce manuscript body text.

## Recommended Operating Model

The preferred operating model is the Productized Regression Pipeline. The researcher provides only project initialization fields, and the agent scaffolds a reproducible project, writes rules, proposes identification and data-processing choices, then runs to each required approval gate. Low-risk work proceeds automatically; P1 risks are recorded; P0 blockers and explicit gates stop the workflow.

If the researcher says `初始化并启动` and provides only project name, paper title, main data, main language, secondary language, and research question, use the default start semantics: initialize the project, create the safe scaffold git commit, enter `PLAN_AUTOPILOT`, and stop at the `Identification Strategy Gate`. Starting does not authorize data cleaning, variable construction, descriptive statistics, regression execution, manuscript prose, causal conclusions, or mechanism claims.

The Detailed workflow below remains authoritative for audit definitions, evidence requirements, and debugging. Use it directly for high-risk projects or when a stage must be inspected in isolation.

## Productized Regression Pipeline

### Candidate v0.1 Final Gates

The Productized Regression Pipeline must not advance from exploratory execution to manuscript-ready bundle or handoff by default. The following gates apply across stages:

- High-risk approval gate: generalized approval language such as "approve all" cannot clear weak-identification regressions, small-N models, over-parameterized models, causal language from cross-sectional questionnaire data, index direction, Likert direction, multi-select missingness, cascade-code timing, or transfer to `empirical-paper-agent`. The proposal must state the action, why it is high risk, the downgrade boundary, allowed wording if continued, and whether main-bundle inclusion is allowed.
- Regression table gate: before a table can enter `Tables and Figures` or handoff main evidence, run `scripts/regression_table_gate.py` or perform the same checks. Any hard-gated table is limited to appendix diagnostic or excluded status with reasons in `review/table_output_audit.md`.
- Status convergence gate: before handoff completion, run `scripts/status_convergence_check.py` or perform the same convergence check across review and handoff records. Any conflict between complete and pending/proposal/not-approved/not-built status blocks completion.
- Encoding gate: before handoff completion, run `scripts/encoding_check.py` or perform the same UTF-8/mojibake audit. Damaged text artifacts cannot enter handoff.
- Transfer gate: handoff to `empirical-paper-agent` is blocked unless the handoff package passes all final gates and the researcher separately approves transfer.
- HITL review accessibility gate: any HITL approval stop must generate a centralized review index and list it in the final Stop Message with Markdown links, full relative paths, descriptions, and decisions needed.
- Tables/Figures format gate: before PDF build or final/handoff inclusion, the combined `.tex` must pass `scripts/tables_figures_format_check.py` or an equivalent audit; failures generate `tables_figures_format_audit.md` and block final status.

### Stage 1: Project Bootstrap

- Goal: Create an AEA/DCAS-style project scaffold from project name, title, main data, software languages, owner, and research question.
- Mode: `pipeline-orchestrator` with `PLAN_AUTOPILOT`, backed by `scripts/project_initializer.py`.
- Automatic actions: create safe directories, `PROJECT_RULES.md`, three project rule files, method cards, generic config/do/report templates, and optional initial commit only when explicitly requested and safe.
- Stop condition: invalid project name, unsafe overwrite, raw-data Git exposure, missing template directory, commit failure, or bootstrap completion.
- Expected outputs: `PROJECT_RULES.md`, `rules/reproducibility-rules.md`, `rules/data-processing-rules.md`, `rules/disclosure-and-license-rules.md`, and `references/method-cards/*.md`.

All stopping stages follow the `Stop Message Contract`: the final user-facing reply must use the fixed `## Stop Message` template and state `why stopped`, `current status`, `current problems`, `questions for researcher`, `blocked boundary`, `required user action`, `next action after response`, and `project record paths` when execution stops for a P0 blocker, approval gate, manual review, handoff transfer gate, final handoff status, or execution beyond approved scope. The message must directly list current problems and answerable researcher questions; if none exist, write `current problems: none` or `questions for researcher: none`. P1/P2 risks do not trigger stops by themselves, but they must be disclosed when the workflow stops for another reason.

In Stop Messages, keep the fixed field names in English but write field values in Chinese whenever practical, because these are user-facing judgment materials. Keep variables, formulas, code, paths, commands, schema fields, Stata package names, model names, and other technical identifiers in their original form. This rule does not apply to formal tables, figures, captions, table notes, figure notes, titles, labels, legends, Appendix Table A, or LaTeX/RTF/XLSX bundles, which must not be Chinese-localized by the Stop Message language rule.

Researcher-facing proposal, decision, gate, and risk-register Markdown files should also use Chinese prose whenever practical. This includes approval-gate artifacts such as `review/*proposal*.md`, `review/*decision*.md`, `review/*gate*.md`, and `review/*risk*.md`. Keep variables, formulas, code, paths, commands, schema fields, status values, decision enums, Stata package names, model names, and machine-readable blocks in their original form. This rule does not apply to formal empirical tables, figures, captions, table notes, figure notes, titles, labels, legends, Appendix Table A, or LaTeX/RTF/XLSX bundles.

HITL approval accessibility rule: before any approval gate final response, create a researcher-facing review index at `review/HITL_REVIEW_INDEX.md` or a stage-specific path such as `review/hitl/HITL_REVIEW_INDEX_pre_execution.md`. The index must show current gate, workflow status, approved items, unapproved items, review-file list, full relative paths, purposes, focus questions, and copyable `APPROVE`, `REVISE`, and `REJECT` reply templates. Every file entry must include both a Markdown link and `Path: \`projects/<project_id>/...\``. The final Stop Message must list the review index first and then the key files, with short descriptions and approval decision needed.

Use this fixed template:

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

### Stage 2: Identification Strategy Gate

- Goal: Read the research question and data structure, then propose feasible identification strategies without executing regressions.
- Automatic actions: identify candidate outcome, treatment, unit, time, proxy variables, treatment assignment mechanism, identification-tree path, feasible designs, rejected designs, diagnostic commands, and P0/P1 risks.
- If unit, time, treatment, outcome, or design details are missing, generate an `Identification Gate Author Questions` section in the user-facing stop message and project planning record. Group questions as `must answer before identification proposal`, `can be supplied later`, and `answer only if external/linkable data exist`.
- The question set must cover observation unit, time structure, treatment/exposure measurement, outcome measurement, mechanism or mediator data, merge/linkage fields, data license and confidentiality boundaries, and intended evidence positioning.
- Stop condition: researcher approval of a design family, request to revise, unclear treatment assignment, or P0 identification boundary.
- Expected outputs: `review/identification_strategy_proposal.md` and linked method-card references.

### Stage 3: Data Processing Gate

- Goal: Propose auditable data-processing rules before any cleaning or variable construction.
- Automatic actions: inspect data dictionaries and safe previews; propose unit, time, primary keys, merge keys, deduplication, sample boundaries, missing handling, unreasonable values, outlier handling, variable units, frequency alignment, panel balance, event windows, multiple treatment handling, control-group definition, variable formulas, leads/lags, and geographic or industry matching rules.
- Stop condition: researcher approval, revise-and-resubmit, or P0 data risk.
- Stop message detail: use the fixed `## Stop Message` template; in `questions for researcher`, list the data-processing rules awaiting approval, especially sample screening, merge keys, deduplication, missing handling, unreasonable-value handling, outlier handling, variable formulas, event windows, multiple treatment rules, and control-group rules.
- Expected outputs: `review/data_cleaning_proposal.md`, `review/cleaning_decision_log.md`, `config/sample_flow.csv`, and updated `rules/data-processing-rules.md` when approved.

### Stage 3.5: Pre-Execution Analysis Approval Gate

- Goal: After identification strategy approval but before execution, consolidate data processing rules, variable formulas, sample rules, controls, estimator, standard errors, clustering, and table plan into a single accessible approval package.
- Automatic actions: generate Markdown review files under `output/plans/` and `review/hitl/`, including `output/plans/01_identification_strategy_summary.md`, `output/plans/02_pre_execution_analysis_plan.md`, `output/plans/03_data_processing_rules.md`, `output/plans/04_variable_construction_plan.md`, `output/plans/05_sample_rules.md`, `output/plans/06_estimator_and_se_plan.md`, `output/plans/07_table_figure_plan.md`, `output/plans/08_risk_and_downgrade_statement.md`, `review/hitl/pre_execution_approval_checklist.md`, and `review/hitl/HITL_REVIEW_INDEX_pre_execution.md`.
- Stop condition: approval, revise-and-resubmit, rejection, or P0 data/specification risk.
- Stop message detail: start with `Workflow paused at: Pre-Execution Analysis Approval Gate`, list `[HITL Review Index](projects/<project_id>/review/hitl/HITL_REVIEW_INDEX_pre_execution.md)` with `Path:`, then list the key review files with Markdown links, full relative paths, short descriptions, and approval decisions needed.
- Blocked boundary: no data cleaning, variable construction, descriptive statistics, regression execution, table generation, or PDF/handoff assembly until the researcher approves the required items.

### Stage 4: Descriptive Statistics And Visualization

- Goal: Generate traceable descriptive statistics and visual diagnostics from approved cleaned data.
- Automatic actions: sample-flow summaries, missingness, distributions, correlation or balance diagnostics, and reproducible descriptive figures.
- Stop condition: missing approved data, incomplete logs, or researcher request for output list changes.
- Expected outputs: descriptive tables, figures, logs, inventories, and audit records.

### Stage 5: Baseline Regression Gate And Execution

- Goal: Propose and execute only researcher-approved main regression specifications.
- Researcher approval required for fixed effects, clustering, controls, estimator, standard-error format, decimal precision, and table structure.
- Default rules: use `absorb()` for fixed effects, explicitly declare clustered standard errors, store estimates with stable names, and prohibit hidden `if` conditions or undeclared sample filters.
- Fixed Effects Decision Node: every baseline proposal must compare `TWFE vs mixed regression` before execution approval. TWFE uses a time dimension plus the best available spatial, individual, or group dimension; mixed regression uses one candidate FE dimension and keeps another candidate dimension as ordinary controls to preserve identifying variation; no FE is only a technical exception when no usable FE dimension exists, FE are fully collinear with the key variables, or sample sparsity/degrees-of-freedom constraints make FE models non-estimable.
- Stop message detail: use the fixed `## Stop Message` template; in `questions for researcher`, list the baseline specification items awaiting approval, including outcome, treatment, sample, fixed effects, clustering, controls, estimator, weights if any, standard-error format, and expected table structure.
- Expected outputs: approved `regression_specs.yml`, baseline logs, stored estimates, exported tables, run report, and failure record.

### Stage 6: Robustness Matrix Gate And Parallel Execution

- Goal: Build a researcher-approved robustness matrix covering estimator, control set, sample range, and outcome-variable dimensions.
- Automatic actions after approval: estimator-agent writes per-cell JSON outputs; reviewer-agent reads JSON and generated outputs to audit direction consistency, sample sizes, stars, standard errors, and figure labels.
- Stop condition: unapproved matrix, execution beyond matrix, failed core cell without failure record, or untraceable table.
- Stop message detail: use the fixed `## Stop Message` template; in `current problems` and `questions for researcher`, list the robustness matrix cells or dimensions awaiting approval, any attempted execution beyond the approved matrix, failed core cells, and the required decision or rerun action.
- Expected outputs: `config/robustness_matrix.yml`, `output/tables/tab_robustness.tex`, `review/robustness_run_report.md`, and `review/robustness_anomalies.md`.

### Stage 7: Tables, Figures, Reproduction Package

- Goal: Export final empirical artifacts and assemble a reproducible handoff package without manuscript prose.
- Automatic actions: LaTeX tables, PNG figures, source-log inventories, evidence map, failed-regression disclosure, replay instructions, and handoff package assembly.
- Stop condition: final handoff completion, P0 traceability gap, or researcher decision about transfer to `empirical-paper-agent`.
- Stop message detail: use the fixed `## Stop Message` template; in `current status` and `current problems`, list missing or completed handoff artifacts, P0/P1/P2 status, failed or blocked outputs, replay status, and handoff package path; in `questions for researcher`, list the explicit decision needed before transfer to `empirical-paper-agent`.
- Expected outputs: final tables, figures, consolidated standalone `Tables and Figures` plus `Appendix` `.tex` when preparing manuscript-ready table delivery, logs, inventories, `handoff_package/`, final audit, and remaining-risk notes.

Before final bundle construction, every regression table must pass the regression table hard gate. A table with small N, R-sq equal or near 1 without explanation, all-missing standard errors, insufficient degrees of freedom, too many parameters for the sample, serious Stata omitted/collinearity/no-standard-error/insufficient-observation signals, or unexplained large estimation-sample loss must be marked `appendix_diagnostic` or `excluded` and must not be treated as manuscript-ready evidence.

Tables and Figures plus Appendix LaTeX bundle rule: the consolidated `.tex` is an empirical artifact only. It must start with `Tables and Figures`, place `Appendix` after the main table/figure section, contain no manuscript body text, include only audited official evidence by default, exclude `validation_cross_check_evidence` unless explicitly requested as a validation appendix, and provide notes for every table and figure. Core facts, main regressions, and key story-related intermediate or mechanism-related evidence belong in `Tables and Figures`; sample composition, variable descriptions, auxiliary cross-tabs, diagnostics, repetitive robustness, and less central evidence belong in `Appendix`. Final displayed variable labels must use approved short labels: one word by default and no more than two words. Notes must explain what Y and X represent, including proxy language where applicable, not only name variables; complex construction can be summarized with details referred to Appendix Table A. Appendix Table A: Variable Definitions must appear before other appendix tables unless the researcher explicitly approves another order. It must use columns `Variables`, `Definition`, and `Data Source`, bold module headings in the order `Dependent Variables`, `Independent Variables`, `Mechanism Variables`, `Moderating Variables`, and `Controls`, one blank row between modules, and place IV variables plus DID terms under `Independent Variables`. Figures without notes are P0 for combined export.

Tables and Figures layout rule: notes must be centered with the table body or placed in centered `threeparttable`/`tablenotes`; descriptive statistics and regression numbers must be formatted before export using 0 decimals for `N` and 3 decimals for means, dispersion, quantiles, correlations, coefficients, standard errors, and p-values unless a documented integer/category exception applies; Table 2 and later main tables must have `\clearpage` or `\newpage` before them; `Appendix` must be after the last main artifact, preceded by `\clearpage`, and centered; wrapper code must not add `Table x:` when the title already contains `Table x.`. Before PDF compilation or final status, run `scripts/tables_figures_format_check.py` or an equivalent audit. If audit fails, generate `tables_figures_format_audit.md`, do not mark the bundle final, and do not include it in handoff main evidence.

Appendix-only bundles are allowed only when the researcher explicitly requests appendix-only delivery, a validation appendix, or a standalone Appendix file.

## Cross-Stage Significance Rule

The agent may report how estimates, standard errors, p-values, or stars vary across pre-declared specifications. It must not select or recommend data cleaning, sample restrictions, variable construction, model specifications, clustering, estimator choice, or table inclusion because the result is more statistically significant.

## Detailed Workflow

## Stage 0: Project Intake

- Goal: Establish the project boundary, owner, software environment, data locations, output expectations, and confidentiality constraints.
- Required inputs: Project metadata draft, data-source list, author notes, expected empirical outputs, software requirements.
- Allowed actions: Inventory provided materials, create missing metadata fields, list unavailable inputs.
- Forbidden actions: Run cleaning or regressions, infer missing specs, create concrete results.
- Expected outputs: Completed or gap-marked `project_metadata`, intake gap list, initial P0/P1/P2 status.
- Human checkpoint: Confirm project scope and whether missing inputs are genuinely unavailable.
- P0/P1/P2 risks: P0 if project owner, raw-data locations, or output scope are unknown; P1 if software versions are uncertain; P2 if naming conventions are incomplete.

## Stage 1: Material Map and Metadata Audit

- Goal: Build a traceable map of raw data, derived data, code, logs, notes, and expected outputs.
- Required inputs: Filesystem inventory, project metadata, author notes.
- Allowed actions: Check paths, classify files, record provenance, identify duplicates and missing metadata.
- Forbidden actions: Modify raw data, delete files, treat undocumented files as final evidence.
- Expected outputs: Material map, provenance notes, metadata audit findings.
- Human checkpoint: Confirm ambiguous file roles and provenance.
- P0/P1/P2 risks: P0 if core data cannot be located; P1 if provenance is incomplete; P2 if file names are inconsistent.

## Stage 2: Data Audit

- Goal: Verify raw and derived data availability, keys, structure, missingness, and documented constraints.
- Required inputs: Material map, data dictionary, raw-data paths, existing cleaning scripts if any.
- Allowed actions: Read data, inspect variables, check keys, report missingness, compare dictionaries to files.
- Forbidden actions: Modify raw data, drop observations, recode variables, overwrite derived data.
- Expected outputs: Data audit report, key checks, missingness summary, unresolved data questions.
- Human checkpoint: Confirm handling of undocumented variables, ambiguous keys, and data anomalies.
- P0/P1/P2 risks: P0 if raw data are altered or key files are unreadable; P1 if key uniqueness or missingness affects planned specs; P2 if labels are incomplete.

## Stage 3: Data Cleaning Proposal

- Goal: Propose reproducible cleaning rules before execution.
- Required inputs: Data audit report, author notes, project metadata, known sample restrictions.
- Allowed actions: Draft cleaning plan, list transformations, specify logs and outputs.
- Forbidden actions: Execute unapproved sample restrictions, winsorize, trim, or drop outliers.
- Expected outputs: Cleaning proposal, sample-flow plan, risk list.
- Human checkpoint: Researcher approval of sample screening, recodes, missing handling, outlier handling, and output paths.
- P0/P1/P2 risks: P0 if sample rules are unapproved; P1 if cleaning choices are researcher-dependent; P2 if comments or labels are sparse.

## Stage 4: Variable Construction Proposal

- Goal: Specify variable formulas and source fields before construction.
- Required inputs: Data dictionary, author notes, cleaning proposal, variable requirements.
- Allowed actions: Draft formulas, dependencies, units, labels, and validation checks.
- Forbidden actions: Invent variables, construct undocumented proxies, change formulas for significance.
- Expected outputs: Variable construction proposal, variable map template, validation checklist.
- Human checkpoint: Researcher approval of formulas, units, missing handling, and source fields.
- P0/P1/P2 risks: P0 if key variable formulas are unconfirmed; P1 if proxy interpretation is uncertain; P2 if labels need polishing.

Questionnaire variables require codebook audit before construction. The audit must classify question type, whether codes represent real quantities/time or option order, Likert direction, missing-value meaning, multi-select semantics, skip logic, reverse coding, and whether sum/mean/index construction is allowed. If these cannot be confirmed, create only proposal variables or descriptive variables; do not construct strong-meaning variables.

## Stage 5: Descriptive Statistics

- Goal: Generate descriptive outputs from approved cleaned data and variable definitions.
- Required inputs: Approved cleaning rules, approved variable definitions, executable scripts, output schema.
- Allowed actions: Run descriptive tables, sample-flow summaries, and reproducible descriptive figures.
- Forbidden actions: Interpret descriptive patterns as causal evidence, hand-fill statistics, omit sample-flow changes.
- Expected outputs: Descriptive tables, figures, logs, sample-flow artifacts, audit records.
- Human checkpoint: Confirm final descriptive output list and table order if needed.
- P0/P1/P2 risks: P0 if outputs lack logs; P1 if descriptive sample differs from regression sample; P2 if formatting needs cleanup.

## Stage 6: Baseline Regression Proposal

- Goal: Lock the main regression specification before execution.
- Required inputs: Approved variables, sample rules, author notes, regression spec draft.
- Allowed actions: Draft `regression_specs` records, identify required packages, list expected tables, and document the Fixed Effects Decision Node comparing TWFE, mixed regression, and no-FE technical exceptions.
- Forbidden actions: Choose main specification independently, change FE or clustering, add controls for significance.
- Expected outputs: Baseline specification proposal, expected-output map, P0 gate status.
- Human checkpoint: Researcher approval of dependent variable, key variable, controls, FE, clustering, estimator, weights, and sample filter.
- P0/P1/P2 risks: P0 if main spec is unconfirmed; P1 if estimator choice needs justification; P2 if model labels are unclear.

## Stage 7: Baseline Regression Execution

- Goal: Execute approved baseline regressions and export traceable outputs.
- Required inputs: Approved `regression_specs`, cleaned data, variable map, Stata do files.
- Allowed actions: Run do files, capture logs, store estimates, export tables, record failures.
- Forbidden actions: Modify approved specs during execution, treat failed regressions as success, manually edit numbers.
- Expected outputs: Baseline logs, exported tables, regression run report, failed-regressions record if applicable.
- Human checkpoint: Confirm how to handle failures, unexpected samples, or package/runtime issues.
- P0/P1/P2 risks: P0 if regression fails or table cannot be traced; P1 if sample sizes differ materially from expectation; P2 if table formatting is imperfect.

## Stage 8: Event Study / Dynamic Effects

- Goal: Execute approved dynamic-effect specifications.
- Required inputs: Approved event-study window, omitted period, event-time variable definition, baseline linkage.
- Allowed actions: Run event-study models, export coefficients and figures, audit omitted period and window.
- Forbidden actions: Change window or omitted period without approval, suppress unfavorable periods, interpret dynamics as proof of mechanism.
- Expected outputs: Event-study logs, coefficient tables, figures, audit notes.
- Human checkpoint: Researcher approval of window, omitted period, binning, and figure/table order.
- P0/P1/P2 risks: P0 if omitted period is unclear; P1 if sparse event-time cells affect interpretation; P2 if axis labels need cleanup.

## Stage 9: Robustness Matrix

- Goal: Execute approved robustness checks linked to baseline specs.
- Required inputs: Approved robustness matrix, baseline spec IDs, scripts, expected outputs.
- Allowed actions: Run robustness checks, export tables, compare specs to matrix, record deviations.
- Forbidden actions: Add or remove robustness checks after seeing significance unless approved, hide failed checks.
- Expected outputs: Robustness logs, tables, figures if any, robustness audit records.
- Human checkpoint: Researcher approval of robustness matrix and any deviations from baseline.
- P0/P1/P2 risks: P0 if matrix is unapproved or outputs lack logs; P1 if sample changes are large; P2 if appendix labels need refinement.

## Stage 10: Heterogeneity and Mechanism-Related Regressions

- Goal: Execute approved subgroup and mechanism-related regression designs.
- Required inputs: Approved design, subgroup definitions, mechanism-related variables, source specs.
- Allowed actions: Run approved models, export outputs, label evidence type precisely.
- Forbidden actions: Treat heterogeneity as mechanism by default, write causal mechanism conclusions, invent channel evidence.
- Expected outputs: Heterogeneity/mechanism-related tables, logs, evidence classification, risk notes.
- Human checkpoint: Researcher approval of subgroup definitions, mechanism-related variables, and output labels.
- P0/P1/P2 risks: P0 if design is unapproved; P1 if evidence is weak or proxy-based; P2 if titles need clearer wording.

## Stage 11: Table and Figure Export

- Goal: Produce final-format reproducible empirical outputs.
- Required inputs: Passed or pending-audit outputs, table schema, figure specs, final table order.
- Allowed actions: Export `rtf`, `tex`, `xlsx`, consolidated standalone `Tables and Figures` plus `Appendix` `.tex`, appendix-only `.tex` only when explicitly requested, and reproducible figures; align labels and notes to specs.
- Forbidden actions: Manually fill numbers, retain blank statistic rows, mismatch titles and specs, interpret unaudited tables.
- Expected outputs: Final tables, final figures, consolidated `Tables and Figures` plus `Appendix` `.tex` when requested or preparing manuscript-ready table delivery, table inventory, figure inventory, export logs.
- Human checkpoint: Researcher approval of final table order and output formats.
- P0/P1/P2 risks: P0 if table values are not generated by code, a consolidated bundle includes cross-check artifacts as official evidence, `Appendix` appears before `Tables and Figures`, Appendix Table A is missing or malformed, any displayed variable label exceeds two words, notes only name Y/X without explaining represented constructs or proxy status, any included table or figure lacks notes, or combined `.tex` has non-environment compile errors; P1 if notes omit other key model details; P2 if formatting is not journal-polished.

## Stage 12: Regression Audit

- Goal: Verify traceability from specs to scripts, logs, outputs, and audit records.
- Required inputs: Specs, scripts, logs, tables, figures, sample-flow records, failed-regressions record.
- Allowed actions: Match output columns to specs, verify FE/clustering/controls/sample, flag gaps.
- Forbidden actions: Repair evidence gaps by inference, pass outputs without logs, ignore failures, edit numerical results, alter specifications, or relabel failed outputs as passed.
- Expected outputs: Final regression audit, P0 status, P1 risk register, evidence map.
- Human checkpoint: Confirm remediation or acceptance of disclosed P1 risks.
- P0/P1/P2 risks: P0 if core outputs cannot be traced; P1 if caveats affect use; P2 if inventories need readability improvements.

## Stage 13: Handoff Package

- Goal: Assemble a complete package for reproduction and possible transfer to `empirical-paper-agent`.
- Required inputs: Passed audit records, output inventories, logs, scripts, risk reports.
- Allowed actions: Copy or index approved artifacts, create handoff README, summarize run status and risks.
- Forbidden actions: Add manuscript prose, omit failed regressions, transfer without researcher approval.
- Expected outputs: Handoff package containing required directories and reports.
- Human checkpoint: Researcher confirms whether to hand off to `empirical-paper-agent`.
- P0/P1/P2 risks: P0 if handoff lacks required core artifacts; P1 if known limitations are not prominent; P2 if package navigation is clunky.

Before marking handoff complete, the builder must run or document equivalent checks for regression-table hard gates, final status convergence, encoding integrity, and executed-variable-map provenance. Handoff packages must not include proposal-only, pending, not-executed, unapproved, or unverified materials as final evidence. If any final gate fails, generate a blocking status report instead of `handoff complete`.

## Stage 14: Replay Validation

- Goal: Validate that the package can be rerun or replayed from documented instructions.
- Required inputs: Handoff package, run order, software notes, scripts, logs.
- Allowed actions: Re-run or dry-run documented steps, compare regenerated outputs, report differences.
- Forbidden actions: Rewrite history, overwrite final artifacts without versioning, claim replay success without logs.
- Expected outputs: Replay validation report, regenerated-output comparison, final blocker status.
- Human checkpoint: Researcher confirms accepted replay differences or requests remediation.
- P0/P1/P2 risks: P0 if replay fails for core outputs; P1 if environment-specific differences remain; P2 if instructions need clarification.
