# Table Style Guide

This guide governs empirical table and figure outputs. The goal is traceability, reproducibility, and accurate labeling.

## Traceability

Every table must map:

- Table ID to output file.
- Column IDs to `spec_id` values.
- `spec_id` values to source do files.
- Source do files to logs.
- Logs to exported numerical outputs.
- Outputs to audit records.

Every figure must map:

- Figure ID to output file.
- Figure data or coefficients to source script.
- Source script to log.
- Figure settings to an approved spec or documented command.

## Numerical Source Rules

- Table numbers must come from Stata output or another approved executable export.
- Do not manually fill coefficients, standard errors, p-values, stars, sample sizes, or summary statistics.
- Do not edit exported numerical values by hand.
- If a table must be reformatted, preserve a machine-generated source table and document the formatting step.
- Empty statistic rows must not remain in final outputs unless explicitly marked unavailable.

## Required Table Notes

Each regression table note must state:

- Dependent variable(s), including what each represents and whether it is a proxy.
- Key explanatory variable(s), including what each represents and whether it is a proxy.
- Unit of observation.
- Fixed effects.
- Clustering level.
- Controls.
- Sample.
- Parentheses rule.
- Star rules.
- Weighting, if used.
- Estimator, if not obvious from the title or column labels.
- Any approved nonstandard sample rule.
- Evidence boundary.

Notes must be factual. They must not include unsupported causal claims or manuscript conclusions.

The Stop Message Chinese-language rule does not apply to table notes or figure notes. Formal table notes and figure notes must remain in English or the separately approved scholarly output language; do not Chinese-localize notes merely because Stop Message field values should be Chinese.

Notes must describe variable meaning, not only variable symbols. Required form:

- "Y is [concept], proxied by [short variable label]."
- "X is [concept], proxied by [short variable label]."
- For DID designs, state the treatment/exposure concept and that the DID term is listed under Independent Variables in Appendix Table A.
- If the proxy or construction is complex, use a concise meaning sentence and add: "Detailed construction is provided in Appendix Table A."

If dependent variable(s), key explanatory variable(s), or controls are too long for concise notes, state the main variable groups and add: "Detailed variable definitions are provided in Appendix Table A."

## Variable Display Labels

Final `Tables and Figures` and `Appendix` bundles must use short presentation labels for variables, not raw long labels or construction descriptions.

- Each displayed variable label in table bodies, column headers, figure axes, legends, and captions must be one word by default and no more than two words.
- Raw dataset names may appear in audit files and variable dictionaries, but final display labels must use the approved `presentation_label`.
- Abbreviations are allowed only when defined in Appendix Table A or standard in the field.
- Do not shorten labels in a way that changes the construct, hides a proxy limitation, or encourages a stronger interpretation than the approved variable definition.
- If a required label cannot be expressed in two words without ambiguity, block final export and request a researcher-approved display label.

## Appendix Table A: Variable Definitions

Every consolidated `Tables and Figures` plus `Appendix` bundle must include Appendix Table A before other appendix tables unless the researcher explicitly approves a different appendix order.

Appendix Table A must be titled `Variable Definitions` and have exactly three columns:

- `Variables`
- `Definition`
- `Data Source`

Rows must be grouped into modules with bold module-heading rows and one blank row between modules. The required module order is:

- **Dependent Variables**
- **Independent Variables**
- **Mechanism Variables**
- **Moderating Variables**
- **Controls**

Other rows must not be bold. IV variables and DID terms belong under **Independent Variables**. The `Definition` column must state the construct and, when relevant, the proxy or construction summary. Complex constructions may refer to approved construction logs or appendix details, but the table still needs a concise definition. The `Data Source` column must name the source dataset or documented source, not only a file path.

## Stata esttab Footer Handling

Raw Stata `esttab` `.tex` files may contain footer notes inside the `tabular` environment. These source files should be preserved as audit evidence, but manuscript-ready combined `.tex` bundles must use one notes system only.

Rules for Stata `esttab` ingestion:

- Remove or migrate esttab footer notes into the final `threeparttable` / `tablenotes` block before insertion into a combined bundle.
- Esttab footer notes include `Standard errors in parentheses`, fixed-effect notes, clustering notes, star-rule notes, evidence-boundary notes, and similar `\multicolumn` footnote rows after `\bottomrule`.
- Do not preserve punctuation-only footer rows, including `\multicolumn{...}{...}{\footnotesize ,}`.
- Do not keep duplicated esttab footer notes inside `tabular` when the final table also has outer `tablenotes`.
- The build or audit report must record whether the esttab footer was removed or migrated.

## Tables and Figures plus Appendix LaTeX Bundles

Final empirical table delivery should support a consolidated standalone `Tables and Figures` plus `Appendix` `.tex` file rather than only scattered table files or a default appendix-only file. The combined bundle is an empirical artifact, not manuscript body text.

Rules for combined bundles:

- The file must compile as standalone XeLaTeX when Chinese titles or notes are present.
- `\begin{document}` must lead directly to `\section*{Tables and Figures}` or an equivalent main table/figure heading.
- `\appendix` and a centered Appendix title must appear after `Tables and Figures`.
- Do not Chinese-localize formal table or figure output because of the Stop Message language rule. Titles, captions, table notes, figure notes, column labels, axis labels, legends, display labels, Appendix Table A content, and LaTeX/RTF/XLSX bundle text must remain in English or the separately approved scholarly output language.
- Do not include Introduction, Results, Robustness, Mechanism, Conclusion, reference-section body content, or manuscript prose.
- Include only audited official tables and figures by default.
- Exclude `validation_cross_check_evidence`, Python cross-check outputs, blocked outputs, pending outputs, failed outputs, and unverified artifacts unless the researcher explicitly requests a validation appendix.
- Every table and figure must have notes.
- Appendix Table A: Variable Definitions must be included before other appendix tables unless a different appendix order is explicitly approved.
- Displayed variable labels in table bodies, column headers, figure axes, legends, and captions must be one word by default and no more than two words.
- Tables should use `threeparttable` and `tablenotes` where practical; wide tables may use `adjustbox` or `resizebox{\textwidth}{!}{...}`.
- Notes must be centered with the table body. Preferred implementation is a centered `threeparttable` with `tablenotes`; standalone notes must use a centered minipage such as `\begin{center}\begin{minipage}{0.92\textwidth}...\end{minipage}\end{center}`. Notes must not align to the page edge by default.
- Regression main tables must hide fixed-effect dummy coefficient rows by default. Fixed effects should be disclosed with `Controls`, `Fixed effects`, and specific FE summary rows plus complete notes. Display individual dummy coefficients only when the researcher explicitly approves that presentation.
- Table titles must display the table number once only. Do not allow wrapper-generated captions such as `Table 1: Table 1. Descriptive Statistics`, `Table.1: Table.1 Descriptive Statistics`, or mixed-language captions such as `表 1: Table 1. Descriptive Statistics`.
- In `Tables and Figures`, Table 1 may follow the section title directly. Table 2 and every later main table must begin after `\clearpage` or `\newpage` unless the researcher explicitly approves a compact version.
- Appendix must appear after the last main table or figure, preceded by `\clearpage`, and centered with a block such as `\begin{center}{\Large \textbf{Appendix}}\end{center}`.
- Appendix Table A must start on the same page as the Appendix title. Do not place `\clearpage` or `\newpage` between the Appendix title and the first appendix table.
- Place core facts, main regressions, and key story-related intermediate or mechanism-related evidence in `Tables and Figures`.
- Place sample composition, variable descriptions, auxiliary cross-tabs, diagnostics, repetitive robustness, and less central evidence in `Appendix`.
- Record placement rationale for every included artifact.
- Do not choose between `Tables and Figures` and `Appendix` based on statistical significance.

Use appendix-only bundles only when the researcher explicitly requests Appendix-only delivery, a validation appendix, or a standalone Appendix file.

Table notes should start with "This table reports" or "This table presents". Figure notes should start with "This figure plots", "This figure shows", "This figure displays", or "This figure reports". Notes may describe sample, unit, variables, model, controls, fixed effects, clustering, parentheses, stars, axes, panels, confidence intervals, and evidence boundaries. Notes must explain what Y and X represent, including proxy language where applicable, rather than only naming Y and X. Notes must not include theory, contribution claims, policy implications, causal conclusions, mechanism proof, or result interpretation.

## Title and Label Rules

- Table titles must match actual content.
- Column names must match actual specifications.
- Table titles, figure titles, column labels, axis labels, legends, captions, table notes, and figure notes must not be Chinese-localized unless the researcher explicitly approved Chinese as the scholarly output language for that final artifact.
- Model labels must be stable across exports.
- Heterogeneity labels must identify the subgroup definition.
- Mechanism-related tables must not be titled as confirmed mechanisms unless the researcher explicitly documents that framing.
- Display labels for variables must be one word by default and no more than two words in final presentation artifacts.

## Supported Formats

Supported table formats:

- `rtf`
- `tex`
- `xlsx`

Additional formats such as `csv`, `html`, or `txt` may be generated for audit or interoperability, but final table expectations should prioritize `rtf`, `tex`, or `xlsx`.

## Formatting Standards

- Final LaTeX tables must use `booktabs` three-line structure where supported: `\toprule`, `\midrule`, and `\bottomrule`. Missing line structure blocks final bundle status unless an equivalent documented table structure is explicitly approved.
- Use consistent decimal places and star rules. Default precision is: `N` 0 decimals; `Mean`, `SD`, `Min`, `P25`, `Median`, `P75`, `Max`, correlations, regression coefficients, standard errors, and p-values 3 decimals unless a variable is documented as integer/categorical and the table-generation logic applies a consistent exception. Raw long decimals must be formatted before final export.
- Keep standard errors, confidence intervals, or p-values clearly labeled.
- Keep sample size and fit statistics aligned with their models.
- Avoid blank rows that imply missing statistics without explanation.
- Keep notes concise and complete.

## Figure Standards

- Figures must be generated by reproducible scripts.
- Figure data must be traceable to approved variables or stored regression output.
- Axes, legends, and captions must match the actual plotted quantity.
- Event-study figures must identify omitted period and window.
- Do not visually suppress failed or omitted estimates without documentation.
- Every Appendix figure must have notes explaining what the figure shows, x-axis, y-axis, groups or panels, confidence intervals if any, unit of observation when relevant, and whether the figure is descriptive or regression-based.

## Audit Requirements

Before a table or figure is final, audit must verify:

- Source files exist.
- Logs exist.
- Output path exists.
- Specs match columns or plotted series.
- FE, clustering, controls, sample, and stars match notes.
- No failed regression is included as successful.
- No manual numerical entry is present.
- Final variable labels satisfy the one-word/default and two-word/maximum display rule.
- Notes explain the represented construct and proxy status for dependent and key explanatory variables.
- Appendix Table A exists, uses the required three columns and module order, places IV and DID terms under Independent Variables, and maps all displayed short labels to definitions and data sources.
- Formal table/figure output is not Chinese-localized unless Chinese was explicitly approved as the scholarly output language for that artifact.
- The final `.tex` passes `scripts/tables_figures_format_check.py` or an equivalent format audit checking duplicate table numbering, mixed Chinese/English duplicate captions, page breaks before Table 2 and later, Appendix order/pagebreak/centering, Appendix-title-to-first-table continuity, note alignment, `booktabs` three-line structure, decimal precision, unresolved placeholders, LaTeX log hard failures such as `Float too large`, PDF existence, and rendered-page QA status. Failed audits must generate `tables_figures_format_audit.md` and block final/handoff main-bundle status.
