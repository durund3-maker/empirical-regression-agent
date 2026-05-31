---
name: table-output-audit
description: Audit empirical rtf, tex, and xlsx tables against specs, scripts, logs, notes, labels, stars, fixed effects, clustering, controls, and failed-regression records. Use to verify traceability without editing numerical results.
---

# table-output-audit

## name
table-output-audit

## description
Use this skill to audit empirical `rtf`, `tex`, and `xlsx` tables for traceability and accuracy against specs, do files, logs, exported numerical outputs, consolidated `Tables and Figures` plus `Appendix` bundles, and appendix-only bundles. For Stata-primary projects, official regression tables should be Stata-generated, preferably through `esttab` / `estout`, and Python/R artifacts can only be accepted as validation or cross-check outputs unless explicitly approved otherwise. It checks column titles, variable names, coefficients, standard errors, stars, N, fixed effects, clustering, controls, notes, blank rows, source links, and whether combined `.tex` bundles include only audited official evidence.

## when_to_use
Use after tables are generated when the user asks to verify table quality, trace numbers to Stata output, find table-fix items, or prepare tables for final audit or handoff.

## required_inputs
- Exported tables in `rtf`, `tex`, `xlsx`, consolidated `Tables and Figures` plus `Appendix` `.tex`, appendix-only `.tex`, or audit-support formats.
- Source do files or executable scripts.
- Complete logs.
- Stata package/export evidence for official Stata tables, including `esttab` / `estout` check or approved fallback.
- Regression specs, table schema, variable dictionary, sample-flow records, and failed-regression records.

## required_outputs
- `output/table_inventory.csv`
- `review/table_output_audit.md`
- `review/table_fix_list.md`
- Combined bundle audit status when a `Tables and Figures` plus `Appendix` `.tex` or appendix-only `.tex` is generated.

## workflow
1. Inventory all target tables and record table ID, title, path, format, linked spec IDs, source scripts, logs, and audit status.
2. Check each table column against spec IDs and expected output mapping.
3. Verify notes state dependent variable(s), key explanatory variable(s), estimator, unit, sample or sample restriction, controls, FE, clustering, parentheses rule, star rules, weights, evidence boundary, and nonstandard sample rules where applicable. Notes must explain what Y and X represent, including proxy language where applicable, not only list variable names. If variable lists or constructions are too long, verify the note includes "Detailed variable definitions are provided in Appendix Table A."
4. For Stata-primary projects, confirm official regression tables were exported from a Stata log-backed run, preferably `esttab` / `estout`; classify Python/R-only output as cross-check unless explicitly approved as a temporary substitute.
5. Compare table values to executable output or logs where feasible; flag unverifiable numbers as P0 or P1 depending on core status.
6. Check for failed regressions included as successful output.
7. Check for blank statistic rows, mismatched labels, unsupported titles, and manual numerical edits.
8. For consolidated `Tables and Figures` plus `Appendix` `.tex` bundles, verify that `Tables and Figures` appears before `\appendix`, no manuscript body text is present, all included tables/figures have notes, placement rationale is recorded for main versus Appendix artifacts, and `validation_cross_check_evidence` is excluded unless explicitly requested as a validation appendix.
9. Verify final displayed variable labels in table bodies, column headers, figure axes, legends, and captions are one word by default and no more than two words, and that each displayed label maps to Appendix Table A.
10. Verify formal table/figure output is not Chinese-localized unless Chinese was explicitly approved as the scholarly output language for that artifact. This check covers titles, captions, table notes, figure notes, column labels, axis labels, legends, display labels, Appendix Table A content, and LaTeX/RTF/XLSX bundle text.
11. Verify Appendix Table A appears before other appendix tables unless an approved exception is recorded; has columns `Variables`, `Definition`, and `Data Source`; uses bold module headings in the order `Dependent Variables`, `Independent Variables`, `Mechanism Variables`, `Moderating Variables`, and `Controls`; leaves one blank row between modules; places IV variables and DID terms under `Independent Variables`; and includes all variables used in final tables, figures, captions, and notes.
12. For Stata `esttab` tables inside combined bundles, verify esttab footer notes are removed or migrated into outer `tablenotes`; do not allow duplicated esttab footer plus `tablenotes`, and do not allow punctuation-only footer rows such as `\multicolumn{...}{...}{\footnotesize ,}`.
13. For appendix-only `.tex` bundles, verify that the first page is Appendix, no manuscript body text is present, all included tables/figures have notes, and `validation_cross_check_evidence` is excluded unless explicitly requested as a validation appendix.
14. Run or document the regression table hard gate for every regression table before final placement. Use `scripts/regression_table_gate.py` when available.
15. Write table audit and fix-list reports without altering empirical numbers.

## regression_table_hard_gate
Any regression table with one or more of the following conditions must be marked `BLOCK_MAIN_BUNDLE` and downgraded to appendix diagnostic or excluded status:

- N below the approved threshold, default `min_n=30`.
- R-sq equal to 1.000 or near 1, default threshold `r2_near_one_threshold=0.995`, without a documented technical explanation.
- Standard errors are all missing, shown as `(.)`, `.`, blank, or equivalent.
- Degrees of freedom are insufficient, or estimated parameters are too numerous for the sample, default `min_obs_per_parameter=5`.
- Linked Stata log or table text contains serious omitted, collinearity, no-standard-error, no-observation, insufficient-observation, or not-estimable signals.
- Actual estimation sample differs materially from the intended or raw sample without explanation, default unexplained loss threshold above 50%.

Hard-gated tables must not be manuscript-ready evidence, must not enter the handoff main-evidence bundle, and must have downgrade reasons written in `review/table_output_audit.md`.

## forbidden_actions
- Do not manually fill or edit coefficients, standard errors, p-values, stars, sample sizes, or summary statistics.
- Do not retain blank statistic rows in final outputs unless explicitly marked unavailable.
- Do not pass a table that lacks spec, do-file, log, and output traceability.
- Do not interpret unaudited tables.
- Do not relabel failed outputs as passed.
- Do not pass Python/R-only regression tables as official Stata results when Stata is the project main language, unless an explicit approved exception labels them correctly.
- Do not pass a consolidated `Tables and Figures` plus `Appendix` bundle or appendix-only bundle if any included table or figure lacks notes.
- Do not pass a consolidated `Tables and Figures` plus `Appendix` bundle, appendix-only bundle, final table, or final figure if output text has been Chinese-localized because of Stop Message language rules.
- Do not pass a consolidated `Tables and Figures` plus `Appendix` bundle if displayed variable labels exceed two words, Appendix Table A is missing, or Appendix Table A fails the required column/module/source checks.
- Do not pass a combined bundle that includes Introduction, Results, Robustness, Mechanism, Conclusion, or other manuscript body prose.
- Do not pass a combined bundle with duplicated Stata `esttab` footer notes inside `tabular` and outer `tablenotes`.
- Do not pass a combined bundle containing `\multicolumn{...}{...}{\footnotesize ,}` or another punctuation-only esttab footer row.
- Do not pass a regression table into a manuscript-ready bundle or handoff main evidence when the regression table hard gate returns `BLOCK_MAIN_BUNDLE`.

## human_review_checkpoint
Researcher confirmation is required for final table order, output formats, title changes that affect interpretation, and any decision to accept disclosed P1 risks.

## P0_risks
- Core table cannot be traced to spec, source do file, log, and output.
- Table numbers appear manually filled or edited.
- Failed regression is included as successful.
- Required log is missing.
- Main language is Stata but the official table is not traceable to Stata do file, Stata log, and Stata-generated export.
- Required `esttab` / `estout` export is missing and no approved fallback is recorded.
- Combined bundle includes `validation_cross_check_evidence` as official evidence.
- Combined bundle contains a table or figure without notes.
- Final table/figure output is Chinese-localized without explicit scholarly-output-language approval.
- Combined bundle uses a final variable display label longer than two words.
- Combined bundle lacks Appendix Table A, has a malformed Appendix Table A, or omits a displayed variable from Appendix Table A.
- `Tables and Figures` plus `Appendix` bundle places Appendix before `Tables and Figures`.
- Combined bundle contains duplicated Stata `esttab` footer notes plus outer `tablenotes`.
- Combined bundle contains `\multicolumn{...}{...}{\footnotesize ,}` or another punctuation-only footer row.
- Regression table notes omit the represented construct or proxy status for dependent variable(s) or key explanatory variable(s), or use only Y/X names without meaning.
- Combined `.tex` cannot compile due to syntax or structure errors, excluding missing local LaTeX tooling.
- Regression table hard gate fails because of small N, R-sq near 1, all-missing standard errors, insufficient degrees of freedom, over-parameterization, serious Stata model warnings, or unexplained sample loss.

## P1_risks
- Notes omit important but recoverable model details.
- Appendix Table A has minor formatting polish issues while all required columns, modules, variables, definitions, and data sources are present.
- Non-core table is pending audit.
- Labels are accurate but may encourage overstatement.

## expected_files
- `output/table_inventory.csv`
- `review/table_output_audit.md`
- `review/table_fix_list.md`
- Exported table files.
- Source scripts and logs.

## evidence_requirements
Table claims require source spec, source script, complete log, exported table, and audit status. In Stata-primary projects, official regression table numbers must come from Stata output, preferably `esttab` / `estout`, unless an approved fallback is recorded. Python/R output is validation/cross-check evidence only by default; no hand entry. Consolidated `Tables and Figures` plus `Appendix` bundles and appendix-only bundles become verified evidence only after source links, placement rationale, notes, exclusion of cross-check artifacts, and compile/static checks pass.

## audit_trail_requirements
Record audited table paths, formats, linked spec IDs, source scripts, logs, checks performed, discrepancies, fix recommendations, and final status.
