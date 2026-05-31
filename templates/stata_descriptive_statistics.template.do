* Purpose: generate approved descriptive statistics for <project_name>.
* Required inputs: <approved_analysis_data_path>, <table_plan_path>.
* Generated outputs: <descriptive_table_path>, <approved_log_path>.
* Maintainer: <maintainer>
* Last updated: <yyyy-mm-dd>
* Stata version: <stata_version>
* Package dependencies: <approved_package_dependencies>
* Log path: <approved_log_path>
* Run order position: descriptive statistics

version <stata_version>
clear all
set more off

global project_root "<project_root>"
global derived_dir "<processed_data_path>"
global table_dir "<table_path>"
global log_dir "<log_path>"

log using <approved_log_path>, replace text

use "<approved_analysis_data_path>", clear

isid <approved_key_fields>
duplicates report <approved_key_fields>

count
keep if <approved_sample_condition>
count

summarize <outcome_var> <treatment_var> <approved_controls>
misstable summarize <outcome_var> <treatment_var> <approved_controls>
tab <time_variable>, missing

* Merge audit placeholder:
* count
* merge <approved_merge_type> <approved_key_fields> using "<approved_using_dataset_path>"
* tab _merge
* count

* Regression visibility placeholder for downstream spec audit:
* <approved_estimator> <outcome_var> <treatment_var> <interaction_terms> <approved_controls>, absorb(<approved_fixed_effects>) vce(cluster <approved_cluster>)

* Export placeholder:
* Export descriptive statistics to <table_path> using approved table command and table_plan.template.csv mapping.

* Failure handling placeholder:
* Record failed descriptive exports or undocumented variables in <table_output_audit_path>.

log close
