# Handoff README: <project_name>

## Package Purpose
This handoff package contains reproducible empirical artifacts, audit records, logs, inventories, and risk disclosures. It is not manuscript prose and must not be treated as causal interpretation.

## Required Package Contents
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

## Run Order
1. Review metadata and approvals: <project_metadata_path>
2. Review data and variable maps: <variable_map_path>
3. Review executed do files and logs: <do_and_log_paths>
4. Review table and figure inventories: <table_inventory_path>, <evidence_map_path>
5. Review final audit and risk reports: <final_regression_audit_path>, <P1_risks_path>

## Key Artifact Paths
- Project root: `<project_root_absolute_path>`
- Tables/Figures bundle: [tables_figures_and_appendix.tex](<relative_tables_figures_tex_path>)  
  Path: `<relative_tables_figures_tex_path>`  
  Absolute Path: `<absolute_tables_figures_tex_path>`
- Tables/Figures PDF: [tables_figures_and_appendix.pdf](<relative_tables_figures_pdf_path>)  
  Path: `<relative_tables_figures_pdf_path>`  
  Absolute Path: `<absolute_tables_figures_pdf_path>`
- Tables/Figures audit: [tables_figures_format_audit.md](<relative_tables_figures_audit_path>)  
  Path: `<relative_tables_figures_audit_path>`  
  Absolute Path: `<absolute_tables_figures_audit_path>`
- PDF rendered-page QA: [pdf_rendered_qa.md](<relative_pdf_rendered_qa_path>)  
  Path: `<relative_pdf_rendered_qa_path>`  
  Absolute Path: `<absolute_pdf_rendered_qa_path>`

## Evidence Classification
- Verified evidence: complete artifact chain with passed audit.
- Author decision: documented researcher approval or note.
- Agent inference: bounded observation from artifacts, not final evidence.
- Open risk: documented unresolved uncertainty.
- Unverified claim: unsupported claim that must not be used as result evidence.

## Transfer Status
- Transfer to empirical-paper-agent approved: <yes|no|pending>
- Approval reference: <author_note_or_config_reference>

## Final Gates
- Regression table gate: <passed|blocked|not_run>
- Status convergence gate: <passed|blocked|not_run>
- Encoding gate: <passed|blocked|not_run>
- Executed variable map gate: <passed|blocked|not_run>
- Static TeX audit status: <passed|blocked|not_run>
- LaTeX log audit status: <passed|blocked|not_run>
- PDF existence status: <passed|blocked|not_run>
- PDF rendered-page QA status: <passed|blocked|not_run|environment_blocker>
- Transfer approval status: <approved|not_approved|pending>

If any gate is blocked, this package is for researcher review only and must not be transferred to `empirical-paper-agent`.
