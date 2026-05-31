* Purpose: export approved and audited empirical tables for <project_name>.
* Required inputs: <approved_estimates_path>, <table_plan_path>.
* Generated outputs: <table_path>, <table_inventory_path>, <approved_log_path>.
* Maintainer: <maintainer>
* Last updated: <yyyy-mm-dd>
* Stata version: <stata_version>
* Package dependencies: <approved_package_dependencies>
* Log path: <approved_log_path>
* Run order position: table export

version <stata_version>
clear all
set more off

global project_root "<project_root>"
global derived_dir "<processed_data_path>"
global table_dir "<table_path>"
global log_dir "<log_path>"

log using <approved_log_path>, replace text

* Load approved estimates or analysis data as required by the approved table workflow.
* estimates use "<approved_estimates_path>"
* use "<approved_input_path>", clear

* Required audit placeholders for table-linked data workflows:
* isid <approved_key_fields>
* duplicates report <approved_key_fields>
* count
* keep if <approved_sample_condition>
* count
* merge <approved_merge_type> <approved_key_fields> using "<approved_using_dataset_path>"
* tab _merge
* count
* summarize <outcome_var> <treatment_var> <approved_controls>
* misstable summarize <outcome_var> <treatment_var> <approved_controls>

* Table mapping placeholder:
* Map <table_id> columns to <spec_id> entries from <table_plan_path>.
* Notes must state approved sample, controls, fixed effects, clustering, estimator, and star rules.

* Example regression visibility placeholder for table-linked rerun workflows:
* <approved_estimator> <outcome_var> <treatment_var> <interaction_terms> <approved_controls>, absorb(<approved_fixed_effects>) vce(cluster <approved_cluster>)

* Export placeholder:
* Export <table_id> to <table_path> in approved formats only.

* Failure handling placeholder:
* Record missing estimates, unmapped columns, empty statistics, failed exports, or manual-number risks in <table_output_audit_path>.

log close
