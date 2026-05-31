# scripts/

Generic helper scripts for `empirical-regression-agent`. These tools support execution audit, inventory building, and handoff assembly. They do not replace `AGENTS.md`, `WORKFLOW.md`, or `agent_core/`, and they must not be used to bypass human confirmation, P0/P1/P2 gating, or evidence rules.

## Script Summary

| Script | Purpose | Read-only by default | May write files | Default dry-run | Requires `--execute` |
| --- | --- | --- | --- | --- | --- |
| `project_initializer.py` | Initialize a productized AEA/DCAS-style project scaffold with `PROJECT_RULES.md`, rule files, method cards, and generic templates. | Yes | Yes, only with `--execute`; optional git commit with `--create-initial-commit` | Yes | Yes |
| `data_safety_check.py` | Report Git-tracked raw/processed data, large files, logs, archives, and sensitive data extensions. | Yes | Yes, only when `--output` is provided | No execution action | No |
| `regression_spec_validator.py` | Validate regression specs for required fields and human confirmation. | Yes | Yes, only when `--output` is provided | No execution action | No |
| `stata_log_parser.py` | Parse Stata logs for failure signals and failed-regression report inputs. | Yes | Yes, only when `--output` is provided | No execution action | No |
| `table_inventory_builder.py` | Inventory exported table files without reading or editing table numbers. | Yes | Yes, requires `--output` | No execution action | No |
| `evidence_map_builder.py` | Build an evidence map from inventories and reports with explicit evidence classes. | Yes | Yes, requires `--output` | No execution action | No |
| `sample_flow_checker.py` | Validate sample-flow records for sample changes and author confirmation. | Yes | Yes, only when `--output` is provided | No execution action | No |
| `stata_runner_wrapper.py` | Print or run an explicit Stata command and optionally parse the resulting log. | Yes | Stata may write logs/outputs only with `--execute` | Yes | Yes |
| `handoff_manifest_builder.py` | Inventory `handoff_package/` and flag missing required handoff artifacts. | Yes | Yes, requires `--output` | No execution action | No |
| `replay_validation.py` | Check framework completeness across rules, config, skills, agents, templates, and scripts. | Yes | Yes, writes validation report | No execution action | No |
| `tables_figures_format_check.py` | Audit combined Tables/Figures `.tex`/log/PDF readiness for duplicate table numbers, mixed captions, page breaks, Appendix placement, centered notes, booktabs structure, long decimals, placeholders, LaTeX log hard failures, and final-bundle readiness. | Yes | Yes, writes audit report | No execution action | No |

## Skill Mapping

- `project_initializer.py`: `project-intake`, `identification-proposal`, `pipeline-orchestrator`
- `data_safety_check.py`: `data-inventory-audit`, `data-cleaning`
- `regression_spec_validator.py`: `regression-spec-audit`, `baseline-regression`, `event-study`, `robustness-checks`, `heterogeneity-mechanism`
- `stata_log_parser.py`: `baseline-regression`, `event-study`, `robustness-checks`, `heterogeneity-mechanism`, `table-output-audit`
- `table_inventory_builder.py`: `table-output-audit`, `handoff-package-builder`
- `evidence_map_builder.py`: `table-output-audit`, `handoff-package-builder`, `regression-spec-audit`
- `sample_flow_checker.py`: `data-cleaning`, `variable-construction`, `data-inventory-audit`
- `stata_runner_wrapper.py`: `descriptive-statistics`, `baseline-regression`, `event-study`, `robustness-checks`, `heterogeneity-mechanism`
- `handoff_manifest_builder.py`: `handoff-package-builder`
- `replay_validation.py`: framework replay and reviewer workflows
- `tables_figures_format_check.py`: `tables-figures-format`, `tables-figures-appendix-builder`, `handoff-package-builder`

## Subagent Mapping

- `dataprep-agent`: `project_initializer.py`, `data_safety_check.py`, `sample_flow_checker.py`
- `estimator-agent`: `regression_spec_validator.py`, `stata_runner_wrapper.py`, `stata_log_parser.py`
- `table-agent`: `table_inventory_builder.py`, `evidence_map_builder.py`, `stata_log_parser.py`
- `reviewer-agent`: `data_safety_check.py`, `regression_spec_validator.py`, `sample_flow_checker.py`, `replay_validation.py`
- `handoff-agent`: `handoff_manifest_builder.py`, `evidence_map_builder.py`, `table_inventory_builder.py`

## Use Limits

- Do not use scripts to create concrete paper claims, manuscript prose, causal conclusions, or mechanism interpretations.
- Do not run Stata unless the relevant human checkpoints are confirmed and `stata_runner_wrapper.py --execute` is explicitly used.
- Do not treat dry-run output as executed work.
- Do not treat inventory presence as verified evidence. Evidence classification still depends on logs, specs, audits, and review status.
- Do not modify raw data. These scripts do not delete or rewrite raw data.
- Scripts that write files require an explicit output path or `--execute`.
- Stata paths, versions, and local environments are never hard-coded.
