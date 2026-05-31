---
name: descriptive-statistics
description: Generate logged descriptive statistics, sample distributions, group comparisons, balance tables, or SMD outputs from approved data and variables. Use for reproducible descriptive outputs that must not be interpreted as causal evidence.
---

# descriptive-statistics

## name
descriptive-statistics

## description
Use this skill to generate reproducible descriptive statistics, sample distributions, group comparisons, balance tables, or standardized mean difference workflows from approved cleaned data and variables. Outputs must be traceable to code, logs, and exported tables, may use three-line table style, and must not be interpreted as causal evidence.

## when_to_use
Use after cleaning and variable construction are approved when the user asks for descriptive tables, balance checks, SMD outputs, sample summaries, or descriptive audit records.

## required_inputs
- Approved cleaned data or derived analysis data.
- Approved variable dictionary and sample-flow records.
- Descriptive output plan or table schema.
- Confirmed table order if final ordering matters.

## required_outputs
- `output/tables/descriptive_statistics.*`
- `output/tables/balance_or_smd.*`
- `output/logs/descriptive_statistics.log`
- `review/descriptive_statistics_audit.md`

## workflow
1. Confirm that input data, variables, and sample rules have passed required gates.
2. Draft or run descriptive-statistics code only from documented variables and approved samples.
3. Generate summary statistics, sample distribution, group comparison, balance, or SMD outputs as specified.
4. Export numbers through Stata or another approved executable process; do not hand-fill table values.
5. Ensure logs capture data loaded, sample counts, commands run, output paths, and errors.
6. Use three-line table style where supported and preserve machine-generated source tables.
7. Audit outputs against variables, sample flow, logs, and table files.

## forbidden_actions
- Do not interpret descriptive differences as causal relationships.
- Do not hand-fill means, standard deviations, SMDs, sample sizes, stars, or notes.
- Do not omit sample-flow changes or hide missingness.
- Do not use undocumented variables.
- Do not write manuscript body text.

## human_review_checkpoint
Researcher confirmation is required for final descriptive output list, grouping variables, balance design, SMD definitions, and final table order when these are not already documented.

## P0_risks
- Descriptive outputs lack a complete log.
- Table values are manually entered or cannot be traced to code.
- Input sample or variables are unapproved.
- Required balance or SMD definitions are missing.

## P1_risks
- Descriptive sample differs materially from regression sample.
- Group definitions are documented but substantively sensitive.
- Some non-core descriptive outputs remain pending audit.

## expected_files
- `output/tables/descriptive_statistics.*`
- `output/tables/balance_or_smd.*`
- `output/logs/descriptive_statistics.log`
- `review/descriptive_statistics_audit.md`

## evidence_requirements
Every statistic must trace to approved data, executable code, complete log, exported table, and audit record. No log, no claim.

## audit_trail_requirements
Record source data, variable dictionary version, sample definition, scripts, logs, table paths, table formats, audit status, and unresolved risks.
