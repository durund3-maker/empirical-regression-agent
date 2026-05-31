* Purpose: execute approved event-study or dynamic-effects specs for <project_name>.
* Required inputs: <approved_analysis_data_path>, <regression_specs_path>, <approved_event_study_window>.
* Generated outputs: <event_study_table_path>, <figure_path>, <approved_log_path>.
* Maintainer: <maintainer>
* Last updated: <yyyy-mm-dd>
* Stata version: <stata_version>
* Package dependencies: <approved_package_dependencies>
* Log path: <approved_log_path>
* Run order position: event study

version <stata_version>
clear all
set more off

global project_root "<project_root>"
global derived_dir "<processed_data_path>"
global table_dir "<table_path>"
global figure_dir "<figure_path>"
global log_dir "<log_path>"

log using <approved_log_path>, replace text

use "<approved_analysis_data_path>", clear

isid <approved_key_fields>
duplicates report <approved_key_fields>

count
keep if <approved_sample_condition>
count

* Event-time construction placeholder:
* generate <event_time_var> = <approved_event_time_formula>
tab <event_time_var>, missing
summarize <event_time_var>
misstable summarize <event_time_var> <outcome_var> <treatment_var> <approved_controls>

* Merge audit placeholder:
* count
* merge <approved_merge_type> <approved_key_fields> using "<approved_using_dataset_path>"
* tab _merge
* count

* Approved dynamic spec: <spec_id>
* Window: <approved_event_window>
* Omitted period: <approved_omitted_period>
<approved_estimator> <outcome_var> <event_time_terms> <approved_controls>, absorb(<approved_fixed_effects>) vce(cluster <approved_cluster>)

* Figure/table export placeholders:
* Export coefficient table to <table_path>.
* Export event-study figure to <figure_path>.

* Failure handling placeholder:
* Record failed dynamic specs, sparse bins, omitted-period issues, or missing figure outputs in <failed_regressions_path>.

log close
