* Purpose: apply researcher-approved cleaning rules for <project_name>.
* Required inputs: <approved_input_path>, <approved_cleaning_rules_path>.
* Generated outputs: <approved_cleaned_data_path>, <approved_log_path>, <sample_flow_path>.
* Maintainer: <maintainer>
* Last updated: <yyyy-mm-dd>
* Stata version: <stata_version>
* Package dependencies: <approved_package_dependencies>
* Log path: <approved_log_path>
* Run order position: data cleaning

version <stata_version>
clear all
set more off

global project_root "<project_root>"
global raw_dir "<raw_data_path_read_only>"
global derived_dir "<processed_data_path>"
global log_dir "<log_path>"

log using <approved_log_path>, replace text

use "<approved_input_path>", clear

isid <approved_key_fields>
duplicates report <approved_key_fields>

count
* Apply only <approved_sample_condition>.
keep if <approved_sample_condition>
count

count
* Apply only <approved_missing_value_rule>.
drop if <approved_missing_condition>
count

misstable summarize <key_id> <time_variable> <outcome_var> <treatment_var> <approved_controls>
summarize <outcome_var> <treatment_var> <approved_controls>

* Regression visibility placeholder for downstream spec audit:
* <approved_estimator> <outcome_var> <treatment_var> <interaction_terms> <approved_controls>, absorb(<approved_fixed_effects>) vce(cluster <approved_cluster>)

* Merge audit placeholder:
* count
* merge <approved_merge_type> <approved_key_fields> using "<approved_using_dataset_path>"
* tab _merge
* count

save "<approved_cleaned_data_path>", replace

* Failure handling placeholder:
* Record any blocked, unapproved, or failed cleaning step in <data_cleaning_proposal_or_audit_path>.

log close
