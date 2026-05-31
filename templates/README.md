# Templates

This directory contains reusable templates for concrete empirical-regression projects. Copy templates into a project workspace only after the relevant intake and human-in-the-loop gates are documented. These templates are not project results, not manuscript prose, and not ready-to-run Stata analysis files until all placeholders are replaced with approved project values.

## Metadata And Config Templates
| Template | Purpose | Recommended project location | Primary subagent | Related skills | Researcher confirmation required |
| --- | --- | --- | --- | --- | --- |
| `project_metadata.template.yml` | Records project scope, data paths, variables, design approvals, forbidden changes, HITL status, and P0 status. | `config/project_metadata.yml` | `dataprep-agent` | `project-intake`, `data-inventory-audit` | Yes |
| `regression_specs.template.yml` | Defines approved specification records and expected outputs. | `config/regression_specs.yml` | `estimator-agent` | `regression-spec-audit`, `baseline-regression`, `event-study` | Yes |
| `robustness_matrix.template.yml` | Defines approved robustness checks and failure/reporting rules. | `config/robustness_matrix.yml` | `estimator-agent` | `robustness-checks` | Yes |
| `variable_dictionary.template.csv` | Maps variables to sources, construction rules, logs, and audit status. | `config/variable_dictionary.csv` or `handoff/variable_map.csv` | `dataprep-agent` | `variable-construction` | Yes for construction rules |
| `table_plan.template.csv` | Maps table columns to specification IDs, formats, logs, and audit status. | `config/table_plan.csv` | `table-agent` | `table-output-audit` | Yes for final table order |
| `tables_figures_appendix.template.tex` | Standalone XeLaTeX Tables and Figures plus Appendix shell for consolidated audited tables and figures with required notes. | `output/tables_figures/tables_figures_and_appendix.tex` | `table-agent` | `tables-figures-appendix-builder`, `table-output-audit` | Yes for final order and main/appendix placement |
| `tables_figures_layout.tex` | Layout fragment showing main-table page breaks, centered notes, single table-number captions, and centered Appendix title. | `output/tables_figures/tables_figures_and_appendix.tex` | `table-agent` | `tables-figures-appendix-builder`, `tables-figures-format` | Yes for final order and compact-version exceptions |
| `table_note_block.tex` | Centered minipage note block for tables or figures that do not use `threeparttable`. | `output/tables_figures/` | `table-agent` | `tables-figures-format` | No, unless note content changes evidence wording |
| `appendix_tables.template.tex` | Appendix-only XeLaTeX shell for explicitly requested standalone Appendix or validation appendix delivery. | `output/appendix/appendix_tables.tex` | `table-agent` | `appendix-latex-builder`, `table-output-audit` | Yes for appendix-only order and inclusion scope |
| `sample_flow.template.csv` | Records auditable sample changes with before/after counts and source logs. | `output/audit/sample_flow.csv` or `handoff/sample_flow.csv` | `dataprep-agent` | `data-cleaning` | Yes for sample rules |
| `evidence_map.template.csv` | Classifies artifacts and claims as verified evidence, author decision, agent inference, open risk, or unverified claim. | `output/audit/evidence_map.csv` or `handoff/evidence_map.csv` | `reviewer-agent` | `handoff-package-builder` | No for audit classification; yes for author decisions |
| `file_manifest.template.csv` | Inventories project files by type, owner stage, source, audit status, and evidence class. | `output/audit/file_manifest.csv` | `reviewer-agent` | `data-inventory-audit`, `handoff-package-builder` | No |

## Stata Do-File Templates
| Template | Purpose | Recommended project location | Primary subagent | Related skills | Researcher confirmation required |
| --- | --- | --- | --- | --- | --- |
| `stata_do_header.template.do` | Shared header pattern for Stata do files. | `do/_header_notes.do` or copied into each do file | `dataprep-agent`, `estimator-agent`, `table-agent` | all Stata-related skills | Yes for paths and run order |
| `stata_master_do.template.do` | Master run-order scaffold. | `do/master.do` | `estimator-agent` | `baseline-regression`, `event-study`, `robustness-checks` | Yes |
| `stata_data_audit.template.do` | Audits IDs, duplicates, missingness, and merge readiness. | `do/01_data_audit.do` | `dataprep-agent` | `data-inventory-audit` | Yes for merge keys |
| `stata_data_cleaning.template.do` | Applies approved sample and cleaning rules with sample-flow counts. | `do/02_data_cleaning.do` | `dataprep-agent` | `data-cleaning` | Yes |
| `stata_variable_construction.template.do` | Constructs approved variables and logs summaries. | `do/03_variable_construction.do` | `dataprep-agent` | `variable-construction` | Yes |
| `stata_descriptive_statistics.template.do` | Generates approved descriptive summaries. | `do/04_descriptive_statistics.do` | `table-agent` | `descriptive-statistics` | Yes for included variables and sample |
| `stata_baseline_regression.template.do` | Executes approved baseline specs with explicit FE and clustering. | `do/05_baseline_regression.do` | `estimator-agent` | `baseline-regression` | Yes |
| `stata_event_study.template.do` | Executes approved dynamic/event-study specs and figure exports. | `do/06_event_study.do` | `estimator-agent` | `event-study` | Yes |
| `stata_robustness.template.do` | Executes approved robustness matrix entries. | `do/07_robustness.do` | `estimator-agent` | `robustness-checks` | Yes |
| `stata_heterogeneity_mechanism.template.do` | Executes approved heterogeneity or mechanism-related designs without converting them into manuscript claims. | `do/08_heterogeneity_mechanism.do` | `estimator-agent` | `heterogeneity-mechanism` | Yes |
| `stata_table_export.template.do` | Exports audited tables mapped to spec IDs. | `do/09_table_export.do` | `table-agent` | `table-output-audit` | Yes for final table order |

## Review And Report Templates
| Template | Purpose | Recommended project location | Primary subagent | Related skills | Researcher confirmation required |
| --- | --- | --- | --- | --- | --- |
| `project_intake_report.template.md` | Summarizes intake scope, available evidence, HITL status, and P0 blockers. | `review/project_intake_report.md` | `dataprep-agent` | `project-intake` | No, except author decisions it records |
| `data_inventory_audit.template.md` | Audits raw-data inventory, IDs, missingness, and merge readiness. | `review/data_inventory_audit.md` | `dataprep-agent`, `reviewer-agent` | `data-inventory-audit` | No |
| `data_cleaning_proposal.template.md` | Proposes sample or cleaning rules before execution. | `review/data_cleaning_proposal.md` | `dataprep-agent` | `data-cleaning` | Yes |
| `variable_construction_audit.template.md` | Audits variable formulas, source fields, logs, and outputs. | `review/variable_construction_audit.md` | `dataprep-agent`, `reviewer-agent` | `variable-construction` | Yes for formulas |
| `regression_spec_audit.template.md` | Checks whether all specification gates are approved before execution. | `review/regression_spec_audit.md` | `estimator-agent`, `reviewer-agent` | `regression-spec-audit` | Yes |
| `regression_run_report.template.md` | Records executed specs, logs, outputs, failures, and risk status. | `review/regression_run_report.md` or `handoff/regression_run_report.md` | `estimator-agent` | `baseline-regression`, `event-study`, `robustness-checks` | No |
| `failed_regressions.template.md` | Records failed or blocked regressions and required next actions. | `review/failed_regressions.md` or `handoff/failed_regressions.md` | `estimator-agent`, `reviewer-agent` | all regression execution skills | No |
| `table_output_audit.template.md` | Audits table-source mapping, notes, failed-regression exclusion, and manual-number risks. | `review/table_output_audit.md` | `table-agent`, `reviewer-agent` | `table-output-audit` | No |
| `final_regression_audit.template.md` | Summarizes final audit scope, checks, passed outputs, failures, and P0/P1/P2 status. | `review/final_regression_audit.md` or `handoff/final_regression_audit.md` | `reviewer-agent` | `handoff-package-builder` | No |
| `handoff_README.template.md` | Documents handoff package contents, run order, evidence classes, and transfer status. | `handoff/handoff_README.md` | `handoff-agent` | `handoff-package-builder` | Yes for transfer to empirical-paper-agent |
| `HITL_REVIEW_INDEX.md` | Centralized HITL approval-gate index with Markdown links, full relative paths, purposes, focus checks, and approval/revise/reject templates. | `review/HITL_REVIEW_INDEX.md` or `review/hitl/HITL_REVIEW_INDEX_<stage>.md` | `reviewer-agent` | `hitl-review`, `pre-regression-proposal` | Yes |
| `pre_execution_approval_checklist.md` | Itemized checklist for data processing, variable formulas, sample rules, controls, estimator, standard errors, clustering, table plan, and high-risk approvals. | `review/hitl/pre_execution_approval_checklist.md` | `reviewer-agent` | `hitl-review`, `pre-regression-proposal` | Yes |

## Generated Project Rules And Method Cards

`scripts/project_initializer.py` generates these project-specific files directly rather than copying them from templates:

- `PROJECT_RULES.md`: project identity, compliance baseline, approval gates, and no-significance-driven-selection rule.
- `rules/reproducibility-rules.md`: path rules, random seed, and software version lock.
- `rules/data-processing-rules.md`: variable naming and data-processing approval gate.
- `rules/disclosure-and-license-rules.md`: AI use disclosure and data license status.
- `references/method-cards/*.md`: compact checklists for DID, modern DID, IV, RDD, synthetic control, matching/DML, and shift-share designs.

## Subagent Usage Summary
- `dataprep-agent`: metadata, data inventory, cleaning proposal, sample flow, variable dictionary, data audit/cleaning/variable-construction do-file templates.
- `estimator-agent`: regression specs, robustness matrix, baseline, event-study, robustness, heterogeneity, and mechanism-related do-file templates plus run reports.
- `table-agent`: descriptive-statistics, table-plan, table-export, tables-figures-appendix-builder, appendix-latex-builder, and table-output-audit templates.
- `reviewer-agent`: evidence map, file manifest, spec audit, table audit, failed-regression audit, and final audit templates.
- `handoff-agent`: evidence map, inventories, failed regressions, final audit, and `handoff_README.template.md`.

## Researcher Confirmation Gates
Researcher confirmation is required before using templates that encode sample-screening rules, merge keys, variable formulas, winsorization or outlier handling, main regression specs, fixed effects, clustering, controls, event-study windows, robustness matrices, heterogeneity or mechanism-related designs, final table order, or transfer to `empirical-paper-agent`.

## Boundary Rules
- Do not create concrete project directories from these templates during framework development.
- Do not run Stata directly from these templates.
- Do not write manuscript body text inside these templates.
- Do not put manuscript body text into Tables and Figures or Appendix LaTeX templates; these bundles may contain section headings, table/figure titles, captions, and notes only.
- Do not insert concrete project variables, coefficients, standard errors, p-values, sample sizes, figure patterns, or table interpretations.
- Replace every placeholder only with documented researcher decisions or verified evidence.
