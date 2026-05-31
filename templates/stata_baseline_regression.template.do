* Purpose: execute approved baseline regression specs for <project_name>.
* Required inputs: <approved_analysis_data_path>, <regression_specs_path>.
* Generated outputs: <baseline_estimates_path>, <table_path>, <approved_log_path>.
* Maintainer: <maintainer>
* Last updated: <yyyy-mm-dd>
* Stata version: <stata_version>
* Package dependencies: <approved_package_dependencies>
* Log path: <approved_log_path>
* Run order position: baseline regression

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

* Approved spec: <spec_id>
* Regression command placeholder; replace only after researcher confirmation.
<approved_estimator> <outcome_var> <treatment_var> <interaction_terms> <approved_controls>, absorb(<approved_fixed_effects>) vce(cluster <approved_cluster>)

* Store and export placeholders:
* estimates store <spec_id>
* Export to <table_path> with column mapped to <spec_id>.

* Failure handling placeholder:
* If _rc != 0, record <spec_id>, this do file, <approved_log_path>, return code,
* and output status in <failed_regressions_path>. Failed specs must not enter final tables.

log close
