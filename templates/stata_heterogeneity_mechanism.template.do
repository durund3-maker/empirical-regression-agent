* Purpose: execute approved heterogeneity or mechanism-related designs for <project_name>.
* Required inputs: <approved_analysis_data_path>, <regression_specs_path>.
* Generated outputs: <heterogeneity_or_mechanism_table_path>, <approved_log_path>.
* Maintainer: <maintainer>
* Last updated: <yyyy-mm-dd>
* Stata version: <stata_version>
* Package dependencies: <approved_package_dependencies>
* Log path: <approved_log_path>
* Run order position: heterogeneity or mechanism-related regression

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

summarize <outcome_var> <treatment_var> <heterogeneity_or_mechanism_var> <approved_controls>
misstable summarize <outcome_var> <treatment_var> <heterogeneity_or_mechanism_var> <approved_controls>

* Merge audit placeholder:
* count
* merge <approved_merge_type> <approved_key_fields> using "<approved_using_dataset_path>"
* tab _merge
* count

* Approved design: <spec_id>
* Design label: <heterogeneity|mechanism_related>
* This template does not convert heterogeneity estimates into mechanism evidence.
<approved_estimator> <outcome_var> <treatment_var> <interaction_terms> <approved_controls>, absorb(<approved_fixed_effects>) vce(cluster <approved_cluster>)

* Export placeholder:
* estimates store <spec_id>
* Export to <table_path> with design label and evidence class.

* Failure handling placeholder:
* Record failed or blocked designs in <failed_regressions_path>.

log close
