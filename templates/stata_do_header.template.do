* Purpose: <do_file_purpose>
* Required inputs: <approved_input_paths>
* Generated outputs: <approved_output_paths>
* Maintainer: <maintainer>
* Last updated: <yyyy-mm-dd>
* Stata version: <stata_version>
* Package dependencies: <approved_package_dependencies>
* Log path: <approved_log_path>
* Run order position: <run_order_position>

version <stata_version>
clear all
set more off

global project_root "<project_root>"
global raw_dir "<raw_data_path_read_only>"
global derived_dir "<processed_data_path>"
global output_dir "<output_path>"
global log_dir "<log_path>"
global table_dir "<table_path>"
global figure_dir "<figure_path>"

log using <approved_log_path>, replace text

display "Template do file started: <do_file_name>"
display "Project root: ${project_root}"

* Input path placeholder: <approved_input_path>
* Output path placeholder: <approved_output_path>

* Required audit placeholders for concrete do files:
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
* Failure handling placeholder: record failures in <failed_regressions_path>.

log close
