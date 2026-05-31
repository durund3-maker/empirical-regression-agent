* Purpose: construct researcher-approved variables for <project_name>.
* Required inputs: <approved_cleaned_data_path>, <variable_dictionary_path>.
* Generated outputs: <approved_constructed_data_path>, <approved_log_path>.
* Maintainer: <maintainer>
* Last updated: <yyyy-mm-dd>
* Stata version: <stata_version>
* Package dependencies: <approved_package_dependencies>
* Log path: <approved_log_path>
* Run order position: variable construction

version <stata_version>
clear all
set more off

global project_root "<project_root>"
global derived_dir "<processed_data_path>"
global log_dir "<log_path>"

log using <approved_log_path>, replace text

use "<approved_cleaned_data_path>", clear

isid <approved_key_fields>
duplicates report <approved_key_fields>

count
* Construct <outcome_var> using <approved_outcome_formula>.
* generate <outcome_var> = <approved_outcome_formula>
count
summarize <outcome_var>
misstable summarize <outcome_var>

count
* Construct <treatment_var> using <approved_treatment_formula>.
* generate <treatment_var> = <approved_treatment_formula>
count
summarize <treatment_var>
tab <treatment_var>, missing

* Construct <approved_controls> using <approved_control_formulas>.
summarize <approved_controls>
misstable summarize <approved_controls>

* Regression visibility placeholder for downstream spec audit:
* <approved_estimator> <outcome_var> <treatment_var> <interaction_terms> <approved_controls>, absorb(<approved_fixed_effects>) vce(cluster <approved_cluster>)

* Merge audit placeholder:
* count
* merge <approved_merge_type> <approved_key_fields> using "<approved_using_dataset_path>"
* tab _merge
* count

save "<approved_constructed_data_path>", replace

* Failure handling placeholder:
* Record unapproved formulas, missing source fields, or failed constructions in <variable_construction_audit_path>.

log close
