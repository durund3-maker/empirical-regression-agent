* Purpose: master run order template for <project_name>.
* Required inputs: approved configs, approved do files, and read-only source data.
* Generated outputs: logs, derived artifacts, tables, figures, and audit records.
* Maintainer: <maintainer>
* Last updated: <yyyy-mm-dd>
* Stata version: <stata_version>
* Package dependencies: <approved_package_dependencies>
* Log path: <approved_log_path>
* Run order position: master

version <stata_version>
clear all
set more off

global project_root "<project_root>"
global do_dir "<project_root>/do"
global log_dir "<log_path>"
global table_dir "<table_path>"
global figure_dir "<figure_path>"
global derived_dir "<processed_data_path>"

log using <approved_log_path>, replace text

display "Master workflow started for <project_name>"
display "Do directory: ${do_dir}"

* Required audit placeholders for called concrete do files:
* use "<approved_input_path>", clear
* isid <approved_key_fields>
* duplicates report <approved_key_fields>
* count
* keep if <approved_sample_condition>
* count
* merge <approved_merge_type> <approved_key_fields> using "<approved_using_dataset_path>"
* tab _merge
* summarize <outcome_var> <treatment_var> <approved_controls>
* misstable summarize <outcome_var> <treatment_var> <approved_controls>
* <approved_estimator> <outcome_var> <treatment_var> <interaction_terms> <approved_controls>, absorb(<approved_fixed_effects>) vce(cluster <approved_cluster>)

* Before execution, confirm all HITL gates are approved in <project_metadata_path>.
* do "${do_dir}/<stata_data_audit_do>"
* do "${do_dir}/<stata_data_cleaning_do>"
* do "${do_dir}/<stata_variable_construction_do>"
* do "${do_dir}/<stata_descriptive_statistics_do>"
* do "${do_dir}/<stata_baseline_regression_do>"
* do "${do_dir}/<stata_event_study_do>"
* do "${do_dir}/<stata_robustness_do>"
* do "${do_dir}/<stata_heterogeneity_mechanism_do>"
* do "${do_dir}/<stata_table_export_do>"

* Failure handling placeholder:
* If any called do file exits with an error, record spec_id, do file, log, return code,
* and output status in <failed_regressions_path>.

display "Master workflow completed for <project_name>"
log close
