* Purpose: audit input data structure and documented metadata for <project_name>.
* Required inputs: <approved_raw_data_path>, <project_metadata_path>.
* Generated outputs: <data_inventory_audit_path>, <approved_log_path>.
* Maintainer: <maintainer>
* Last updated: <yyyy-mm-dd>
* Stata version: <stata_version>
* Package dependencies: <approved_package_dependencies>
* Log path: <approved_log_path>
* Run order position: data audit

version <stata_version>
clear all
set more off

global project_root "<project_root>"
global raw_dir "<raw_data_path_read_only>"
global derived_dir "<processed_data_path>"
global log_dir "<log_path>"

log using <approved_log_path>, replace text

use "<approved_input_path>", clear

count
describe
codebook <key_id> <time_variable> <outcome_var> <treatment_var>

isid <approved_key_fields>
duplicates report <approved_key_fields>

misstable summarize <key_id> <time_variable> <outcome_var> <treatment_var> <approved_controls>
summarize <outcome_var> <treatment_var> <approved_controls>
tab <time_variable>, missing

* Regression visibility placeholder for downstream spec audit:
* <approved_estimator> <outcome_var> <treatment_var> <interaction_terms> <approved_controls>, absorb(<approved_fixed_effects>) vce(cluster <approved_cluster>)

* Merge audit placeholder:
* count
* merge <approved_merge_type> <approved_key_fields> using "<approved_using_dataset_path>"
* tab _merge
* count
* Do not drop _merge before the merge distribution is logged.

* Failure handling placeholder:
* Record missing inputs, duplicate-key failures, merge failures, or undocumented variables in <data_inventory_audit_path>.

log close
