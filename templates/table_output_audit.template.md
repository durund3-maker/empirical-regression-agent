# Table Output Audit: <project_name>

## Audit Scope
- Table plan: <table_plan_path>
- Table outputs: <table_paths>
- Source do files: <do_file_paths>
- Source logs: <log_paths>

## Key Artifact Paths
- Table plan: [table_plan](<table_plan_path>)  
  Path: `<table_plan_path>`  
  Absolute Path: `<absolute_table_plan_path>`
- Tables/Figures format audit: [tables_figures_format_audit.md](<tables_figures_format_audit_path>)  
  Path: `<tables_figures_format_audit_path>`  
  Absolute Path: `<absolute_tables_figures_format_audit_path>`
- PDF rendered-page QA: [pdf_rendered_qa.md](<pdf_rendered_qa_path>)  
  Path: `<pdf_rendered_qa_path>`  
  Absolute Path: `<absolute_pdf_rendered_qa_path>`

## Evidence Classification
- Verified evidence: <verified_evidence_items>
- Author decision: <author_decision_items>
- Agent inference: <agent_inference_items>
- Open risk: <open_risk_items>
- Unverified claim: <unverified_claim_items>

## Checks
- Columns map to spec IDs: <passed|failed|pending>
- Notes match fixed effects, clustering, controls, sample, estimator, and star rules: <passed|failed|pending>
- No manual table numbers: <passed|failed|pending>
- Empty statistic rows handled: <passed|failed|pending>
- Failed regressions excluded: <passed|failed|pending>
- Regression table hard gate: <passed|blocked|not_applicable>
- Static TeX format audit: <passed|failed|pending|not_applicable>
- LaTeX log hard-failure audit: <passed|failed|pending|not_applicable>
- PDF existence audit: <passed|failed|pending|not_applicable>
- PDF rendered-page QA: <passed|failed|pending|environment_blocker|not_applicable>

## Regression Table Hard Gate
- Gate script: <scripts/regression_table_gate.py_or_equivalent>
- Gate output: <gate_report_path>
- Tables blocked from main bundle: <table_ids_or_none>
- Downgrade or exclusion reasons: <reasons>
- Appendix diagnostic approval, if any: <approval_reference_or_none>

Any table with small N, R-sq equal or near 1 without explanation, all-missing standard errors, insufficient degrees of freedom, over-parameterization, serious Stata omitted/collinearity/no-standard-error/insufficient-observation signals, or unexplained sample loss must be `appendix_diagnostic` or `excluded`.

## Findings
- P0 findings: <P0_findings>
- P1 findings: <P1_findings>
- P2 findings: <P2_findings>
