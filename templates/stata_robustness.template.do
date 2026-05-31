* Purpose: execute approved robustness checks for <project_name>.
* Required inputs: <approved_analysis_data_path>, <robustness_matrix_path>.
* Generated outputs: <robustness_table_path>, <approved_log_path>.
* Maintainer: <maintainer>
* Last updated: <yyyy-mm-dd>
* Stata version: <stata_version>
* Package dependencies: <approved_package_dependencies>
* Log path: <approved_log_path>
* Run order position: robustness

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

* Merge audit placeholder:
* count
* merge <approved_merge_type> <approved_key_fields> using "<approved_using_dataset_path>"
* tab _merge
* count

* Approved robustness check: <robustness_check_id>
* Deviation from baseline: <approved_robustness_deviation>
<approved_estimator> <outcome_var> <treatment_var> <interaction_terms> <approved_controls>, absorb(<approved_fixed_effects>) vce(cluster <approved_cluster>)

* Export placeholder:
* estimates store <robustness_check_id>
* Export to <table_path> only if run succeeds and is mapped in robustness_matrix.template.yml.

* Failure handling placeholder:
* Record failed robustness checks in <failed_regressions_path>; do not relabel failures as passed.

log close
