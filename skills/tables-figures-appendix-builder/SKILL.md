---
name: tables-figures-appendix-builder
description: Build a single standalone XeLaTeX Tables and Figures plus Appendix file from audited official tables and figures, excluding cross-check artifacts by default and requiring notes for every artifact.
---

# tables-figures-appendix-builder

## name
tables-figures-appendix-builder

## description
Use this skill to assemble audited empirical tables and figures into one consolidated `Tables and Figures` plus `Appendix` `.tex` file. The output is an empirical artifact, not manuscript body text. It must compile as a standalone XeLaTeX document, place story-relevant official evidence in `Tables and Figures`, place auxiliary official evidence in `Appendix`, and contain no introduction, results prose, conclusion, or manuscript interpretation.

This is the default manuscript-ready table/figure bundle. Use `appendix-latex-builder` only when the researcher explicitly requests an appendix-only bundle.

## when_to_use
Use after table-output audit passes, final table/figure order is approved, and the user asks for manuscript-ready tables and figures, an Overleaf-ready empirical artifact, a combined table/figure file, or final table delivery.

## required_inputs
- Audited table plan or table inventory with official evidence classification.
- Official table files, preferably Stata `esttab` `.tex` for Stata-primary projects.
- Figure inventory and figure files, if any.
- Source scripts, logs, and audit reports for all included artifacts.
- Evidence-function classification for each artifact: core fact, main regression, key mechanism/intermediate result, robustness, sample description, variable description, diagnostic, auxiliary cross-tab, or validation/cross-check.
- Approved variable dictionary fields for final presentation: raw variable name, variable role, `presentation_label`, definition, proxy or construction summary, and data source.
- Approved final order and output path.

## required_outputs
- One standalone XeLaTeX `.tex` file, usually `output/tables_figures/tables_figures_and_appendix.tex`.
- Build/audit report listing artifacts included in `Tables and Figures`, artifacts included in `Appendix`, and excluded artifacts.
- `tables_figures_format_audit.md` when the format audit is run; if the audit fails, this report is mandatory and the bundle remains non-final.
- Compile check result or explicit LaTeX-environment blocker.

## default_inclusion_rules
- Include only artifacts with passed audit status and official evidence classification.
- Exclude `validation_cross_check_evidence`, Python cross-check tables, blocked outputs, pending outputs, failed outputs, and unverified artifacts by default.
- Exclude regression tables with `BLOCK_MAIN_BUNDLE` from manuscript-ready `Tables and Figures` and handoff main evidence. They may appear only as explicitly labeled appendix diagnostics when the table-output audit records downgrade reasons and the researcher approves diagnostic inclusion.
- Include cross-check artifacts only if the researcher explicitly requests a validation appendix and the output labels them as validation, not official evidence.
- Descriptive tables may be converted from audited CSV/Markdown, but numerical values must come from executable outputs and must not be hand-filled.
- Official Stata regression tables should use the Stata `esttab` `.tex` output where available.

## stata_esttab_ingestion_rules
When ingesting Stata `esttab` `.tex` output into a `threeparttable` bundle, the builder must treat the Stata file as the audited numerical source, not as final presentation markup.

- Remove or migrate any esttab footer notes before insertion into the final `tabular`.
- Esttab footer notes include `\multicolumn{...}{...}{\footnotesize Standard errors in parentheses}`, fixed-effect notes, clustering notes, star-rule notes, evidence-boundary notes, and similar note rows after `\bottomrule`.
- Do not preserve `\multicolumn{...}{...}{\footnotesize ,}` or any footer row whose substantive content is only punctuation.
- The final manuscript-ready combined `.tex` must have exactly one notes system for each table: the outer `threeparttable` plus `tablenotes`.
- Preserve a machine-generated source table for audit, and record in the build/audit report that the esttab footer was removed or migrated into `tablenotes`.

## evidence_function_placement
Place artifacts by evidence function, not by file creation order.

Put in `Tables and Figures`:
- Core empirical facts needed to understand the paper's main evidence.
- Main regression tables.
- Key intermediate, mechanism-related, or heterogeneity evidence that directly supports the paper story, while preserving exploratory or non-causal labels when required.
- Main figures that summarize the central pattern or research-design diagnostics.

Put in `Appendix`:
- Sample composition and data-coverage tables.
- Variable definitions, descriptive distributions, auxiliary cross-tabs, and balance or missingness diagnostics.
- Repetitive robustness outputs, weak auxiliary evidence, small-sample checks that are not central to the story, and formatting variants.
- Supplemental figures that document construction, diagnostics, or sensitivity rather than the main empirical narrative.

If an artifact is story-relevant but statistically or design-wise fragile, it may remain in `Tables and Figures` only when its caption and notes disclose the exploratory, small-sample, correlational, or non-causal boundary. Do not move an artifact between sections because of statistical significance.

## latex_structure
The generated file must be a standalone XeLaTeX document. `\begin{document}` must be followed directly by the empirical-artifact front matter and the main section:

```tex
\section*{Tables and Figures}
```

The Appendix must follow the main section:

```tex
\clearpage
\begin{center}
{\Large \textbf{Appendix}}
\end{center}
\vspace{1em}
```

The file must not contain manuscript body sections such as Introduction, Literature Review, Research Design, Results, Robustness, Mechanism, or Conclusion. The file may contain table and figure titles, captions, notes, Appendix Table A, and section headings only.

The Appendix must include Appendix Table A: Variable Definitions before other appendix tables unless the researcher explicitly approves a different appendix order.

The Stop Message Chinese-language rule does not apply to this bundle. Final table and figure titles, captions, table notes, figure notes, column labels, axis labels, legends, display labels, Appendix Table A content, and LaTeX/RTF/XLSX bundle text must remain in English or the separately approved scholarly output language.

Use `ctexart` or equivalent XeLaTeX Chinese support when Chinese titles or notes are present. Required packages include `booktabs`, `threeparttable`, `adjustbox`, `caption`, `geometry`, and `graphicx`.

If figures are present, list figures before tables within `Tables and Figures` unless the researcher approves a table-first ordering. Do not insert empty figure placeholders when no official figures exist.

## layout_rules
The builder must enforce polished layout before PDF compilation or final status.

- Notes must be centered with the table body. Prefer `threeparttable` with `tablenotes`; if `threeparttable` is not used, wrap notes in a centered `0.92\textwidth` minipage.
- Numeric values must be formatted before final export. Defaults: `N` uses 0 decimals; `Mean`, `SD`, `Min`, `P25`, `Median`, `P75`, `Max`, correlations, regression coefficients, standard errors, and p-values use 3 decimals unless a documented integer/category exception applies consistently.
- Regression main tables must hide fixed-effect dummy coefficient rows by default. Present fixed effects through `Controls`, `Fixed effects`, and specific FE summary rows plus notes. Include individual dummy coefficient rows only when the researcher explicitly approves that display choice.
- Table 1 may appear immediately after `Tables and Figures`; Table 2 and later main tables must be preceded by `\clearpage` or `\newpage` unless the researcher explicitly approved a compact version.
- `Appendix` must appear after all main tables/figures, must be preceded by `\clearpage`, and must be centered.
- Appendix Table A must begin on the same page as the Appendix title; do not insert `\clearpage` or `\newpage` between the Appendix title and the first appendix table.
- Do not add an outer `Table x:` label when the table title already contains `Table x.` or `Table x`. English final output must not mix Chinese automatic labels with English manual labels such as `表 1: Table 1`. Each table may display one table number only.
- Final LaTeX tables must use a `booktabs` three-line structure with `\toprule`, `\midrule`, and `\bottomrule`, unless an equivalent table structure is explicitly approved and documented.

## notes_rules
Every table and figure must have notes.

- Table notes must start with "This table reports" or "This table presents".
- Figure notes must start with "This figure plots", "This figure shows", "This figure displays", or "This figure reports".
- Notes may state sample, unit, variables, model, controls, fixed effects, clustering level, what is in parentheses, significance-star convention, figure axes, confidence intervals, and evidence boundaries.
- Notes must remain in English or the separately approved scholarly output language. Do not Chinese-localize table notes or figure notes because Stop Message field values should be Chinese.
- Notes must explain what dependent variable(s) and key explanatory variable(s) represent, not only name Y and X. Use wording such as "Y is [construct], proxied by [short label]" and "X is [construct], proxied by [short label]" when the empirical variable is a proxy.
- If a variable proxy or construction is too complex for the note, the note must still state the represented construct and add: "Detailed construction is provided in Appendix Table A."
- Notes must not write theory, contribution claims, policy implications, causal conclusions, mechanism proof, or result interpretation.
- Notes must not invent sample periods, units, variables, confidence intervals, fixed effects, clustering levels, or significance conventions.
- Regression table notes must state dependent variable(s), key explanatory variable(s), estimator, unit of observation, sample or sample restriction, controls, fixed effects, clustering level, parentheses rule, significance-star convention when shown, and evidence boundary.
- If the dependent variable(s), key explanatory variable(s), or controls are too long for concise notes, state the main variable groups and add: "Detailed variable definitions are provided in Appendix Table A."

## variable_label_rules
Final presentation labels must be concise and mapped to Appendix Table A.

- Use approved `presentation_label` values in final table bodies, column headers, figure axes, legends, and captions.
- Each displayed variable label must be one word by default and no more than two words.
- Raw variable names, long survey text, and construction descriptions may remain in audit materials but must not be used as final display labels unless they satisfy the same length rule.
- Do not shorten a label in a way that changes the construct, hides a proxy limitation, or implies a causal claim.
- If no accurate one- or two-word display label exists, block final export and request researcher approval for a short label.

## appendix_table_a_rules
Every consolidated bundle must include Appendix Table A before other appendix tables unless the researcher explicitly approves a different appendix order.

- Caption/title: `Variable Definitions`.
- Columns, in order: `Variables`, `Definition`, `Data Source`.
- Module order: `Dependent Variables`, `Independent Variables`, `Mechanism Variables`, `Moderating Variables`, `Controls`.
- Module headings must be bold; ordinary variable rows must not be bold.
- Leave one blank row between modules.
- IV variables and DID terms must be placed under `Independent Variables`.
- Each variable used in final tables, figure axes, legends, captions, or notes must appear once under the appropriate module.
- The `Definition` cell must state the construct and proxy/construction summary; complex construction may refer to approved construction details, but the construct must still be clear.
- The `Data Source` cell must identify the source dataset or documented source, not only an output file.

## figure_rules
Every included figure must be traceable to an approved figure spec, executable script/log, and output file. Figure notes must state what the figure shows, x-axis, y-axis, groups or panels if any, confidence intervals if any, unit of observation when relevant, and whether the figure is descriptive or regression-based.

If a formal figure lacks notes, the combined bundle is blocked with a P0 issue. Do not silently include note-less figures.

## audit_checks
Before marking the combined bundle passed, verify:

- The `.tex` file is standalone and `Tables and Figures` appears before `\appendix` and `Appendix`.
- Included artifacts are audited official evidence unless explicitly labeled validation appendix.
- Every table and figure has a caption/title and notes.
- Notes match source specs, logs, table plan, and figure inventory.
- Formal table/figure output is not Chinese-localized unless Chinese was explicitly approved as the scholarly output language for that artifact.
- Displayed variable labels satisfy the one-word/default and two-word/maximum rule.
- Notes explain represented constructs and proxy status for dependent and key explanatory variables.
- Appendix Table A exists, appears before other appendix tables unless an approved exception is recorded, has the required three columns, uses the required module order and formatting, places IV and DID terms under Independent Variables, and covers all displayed variables.
- Stata `esttab` footer notes have been removed or migrated into `tablenotes`; no duplicated esttab footer plus outer `tablenotes` remains.
- No `\multicolumn{...}{...}{\footnotesize ,}` footer row remains in any final regression table.
- Placement rationale is recorded for each artifact included in `Tables and Figures` or `Appendix`.
- No Python cross-check or `validation_cross_check_evidence` artifact is included as official evidence.
- The file contains no manuscript body text, result interpretation, causal conclusion, policy implication, or mechanism proof.
- LaTeX compiles with XeLaTeX or, if LaTeX is unavailable, the environment blocker is recorded and static structure checks pass.
- Any LaTeX syntax error in the generated `.tex` is a P0 blocker unless caused solely by missing local LaTeX tooling.
- `scripts/tables_figures_format_check.py` or an equivalent audit passes. Static preflight may run without post-build paths, but final bundle status must use `--final --pdf-path --log-path --rendered-qa-path`. The audit must check duplicate captions such as `Table 1: Table 1`, mixed-language duplicate captions such as `表 1: Table 1`, page breaks before Table 2 and later, Appendix placement after the last main table, Appendix `\clearpage`, centered Appendix title, Appendix-title-to-first-table continuity, centered notes or `threeparttable` notes, `booktabs` three-line structure, uniform decimal precision, long decimals, unresolved placeholders, LaTeX log hard failures such as `Float too large`, PDF existence, and rendered-page QA status.
- If the format audit fails, write `tables_figures_format_audit.md`, do not mark the `.tex` or PDF final, and do not copy the bundle into handoff main evidence.
- Do not mark a bundle final when rendered-page QA is missing, failed, pending, or `environment_blocker`, or when the LaTeX log contains unresolved hard failures. Static TeX pass alone is only preflight status.

## forbidden_actions
- Do not write manuscript body text, results prose, causal conclusions, policy implications, or contribution claims.
- Do not include Introduction, Results, Robustness, Mechanism, Conclusion, or reference-section body content.
- Do not manually edit or enter coefficients, standard errors, p-values, stars, sample sizes, or figure values.
- Do not include unaudited, blocked, failed, pending, or cross-check artifacts as official evidence.
- Do not include any table or figure without notes.
- Do not Chinese-localize final table or figure titles, captions, table notes, figure notes, column labels, axis labels, legends, display labels, Appendix Table A content, or bundle text because of Stop Message language rules.
- Do not use long variable labels in final table bodies, column headers, figure axes, legends, or captions.
- Do not omit Appendix Table A from a consolidated `Tables and Figures` plus `Appendix` bundle.
- Do not preserve duplicated Stata esttab footer notes inside `tabular` when the final table also uses `tablenotes`.
- Do not preserve meaningless punctuation-only esttab footer rows such as `\multicolumn{...}{...}{\footnotesize ,}`.
- Do not choose `Tables and Figures` versus `Appendix` placement based on statistical significance.
- Do not include hard-gated regression tables in manuscript-ready main evidence or handoff main evidence.
- Do not mark a bundle final or handoff-ready when `tables_figures_format_audit.md` reports unresolved format failures, when the LaTeX log has unresolved hard failures, or when rendered PDF QA is missing.

## P0_risks
- Combined `.tex` contains manuscript body text.
- `Tables and Figures` is missing or appears after Appendix.
- Combined bundle includes validation/cross-check artifacts as official evidence.
- A table or figure lacks notes.
- Final table/figure output is Chinese-localized without explicit scholarly-output-language approval.
- A final display label for a variable exceeds two words or is not mapped to Appendix Table A.
- Appendix Table A is missing, lacks the required columns, lacks required modules, places IV or DID terms outside Independent Variables, or omits variables used in the final bundle.
- A regression table has duplicated esttab footer notes and outer `tablenotes`.
- A final table includes `\multicolumn{...}{...}{\footnotesize ,}` or another punctuation-only footer row.
- Regression table notes omit the represented construct or proxy status for dependent variable(s) or key explanatory variable(s), or use only Y/X names without meaning.
- Notes invent unsupported model/sample/variable details or contain causal conclusions.
- Generated `.tex` fails to compile due to structure or syntax errors.
- A hard-gated pathological regression table is included as main evidence.
- The combined `.tex` fails the Tables/Figures format audit for duplicate table numbering, mixed Chinese/English duplicate captions, missing required main-table page breaks, misplaced/non-centered Appendix title, Appendix title separated from Appendix Table A, non-centered notes, missing `booktabs` three-line structure, raw long decimals, unresolved placeholders, LaTeX log hard failures, missing PDF, missing rendered-page QA, or PDF build failure.

## evidence_requirements
Combined bundle artifacts require passed source audits, source scripts/logs, generated outputs, notes, placement rationale, and compile/static LaTeX checks. The combined bundle itself is verified evidence only after its source links, section placement, and notes pass audit.
