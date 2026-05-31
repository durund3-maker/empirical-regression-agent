---
name: appendix-latex-builder
description: Build a single standalone XeLaTeX Appendix file from audited official tables and figures, excluding cross-check artifacts by default and requiring notes for every table and figure.
---

# appendix-latex-builder

## name
appendix-latex-builder

## description
Use this skill to assemble audited empirical tables and figures into one consolidated Appendix `.tex` file. The output is an empirical artifact, not manuscript body text. It must compile as a standalone XeLaTeX document, start with Appendix on the first page, and contain no introduction, results prose, conclusion, or manuscript interpretation.

This is not the default manuscript-ready table/figure bundle. For ordinary final empirical table delivery, use `tables-figures-appendix-builder`, which creates a `Tables and Figures` section followed by `Appendix`.

## when_to_use
Use after table-output audit passes, final table/figure order is approved, and the user explicitly asks for an appendix-only LaTeX bundle, Overleaf-ready appendix, validation appendix, or standalone Appendix file.

Do not use this skill for the default final table/figure delivery when story-relevant artifacts should appear before Appendix.

## required_inputs
- Audited table plan or table inventory.
- Official table files, preferably Stata `esttab` `.tex` for Stata-primary projects.
- Figure inventory and figure files, if any.
- Source scripts, logs, and audit reports for all included artifacts.
- Approved variable dictionary fields for final presentation: raw variable name, variable role, `presentation_label`, definition, proxy or construction summary, and data source.
- Approved final order and output path.

## required_outputs
- One standalone Appendix `.tex` file, usually `output/appendix/appendix_tables.tex`.
- Appendix build/audit report listing included and excluded artifacts.
- Compile check result or explicit LaTeX-environment blocker.

## default_inclusion_rules
- Include only artifacts with passed audit status and official evidence classification.
- Exclude `validation_cross_check_evidence`, Python cross-check tables, blocked outputs, pending outputs, failed outputs, and unverified artifacts by default.
- Include cross-check artifacts only if the researcher explicitly requests a validation appendix and the output labels them as validation, not official evidence.
- Descriptive tables may be converted from audited CSV/Markdown, but numerical values must come from executable outputs and must not be hand-filled.
- Official Stata regression tables should use the Stata `esttab` `.tex` output where available.

## latex_structure
The generated file must be a standalone XeLaTeX document. `\begin{document}` must be followed directly by Appendix front matter, such as:

```tex
\appendix
\section*{Appendix}
```

The file must not contain manuscript body sections such as Introduction, Literature Review, Research Design, Results, Robustness, Mechanism, or Conclusion. The first page is Appendix.

If the appendix-only bundle contains empirical tables or figures that use variable labels, it should include Appendix Table A: Variable Definitions before other appendix tables unless the researcher explicitly approves a different order.

Use `ctexart` or equivalent XeLaTeX Chinese support when Chinese titles or notes are present. Required packages include `booktabs`, `threeparttable`, `adjustbox`, `caption`, `geometry`, and `graphicx`.

## notes_rules
Every table and figure must have notes.

- Table notes must start with "This table reports" or "This table presents".
- Figure notes must start with "This figure plots", "This figure shows", "This figure displays", or "This figure reports".
- Notes may state sample, unit, variables, model, controls, fixed effects, clustering level, what is in parentheses, significance-star convention, figure axes, confidence intervals, and evidence boundaries.
- Notes must explain what dependent variable(s) and key explanatory variable(s) represent, including proxy language where applicable, not only name Y and X.
- If a variable proxy or construction is too complex for the note, the note must still state the represented construct and add: "Detailed construction is provided in Appendix Table A."
- Notes must not write theory, contribution claims, policy implications, causal conclusions, mechanism proof, or result interpretation.
- Notes must not invent sample periods, units, variables, confidence intervals, fixed effects, clustering levels, or significance conventions.
- Regression table notes should state estimator, unit of observation, sample, controls, fixed effects, clustering level, parentheses, and star convention when available.

## variable_definition_rules
Final displayed variable labels should be one word by default and no more than two words in table bodies, column headers, figure axes, legends, and captions. Each displayed label must map to Appendix Table A when the bundle includes empirical variables.

Appendix Table A must use columns `Variables`, `Definition`, and `Data Source`; bold module headings in the order `Dependent Variables`, `Independent Variables`, `Mechanism Variables`, `Moderating Variables`, and `Controls`; one blank row between modules; and IV variables and DID terms under `Independent Variables`.

## figure_rules
Every included figure must be traceable to an approved figure spec, executable script/log, and output file. Figure notes must state what the figure shows, x-axis, y-axis, groups or panels if any, confidence intervals if any, unit of observation when relevant, and whether the figure is descriptive or regression-based.

If a formal figure lacks notes, the appendix build is blocked with a P0 issue. Do not silently include note-less figures.

## audit_checks
Before marking the Appendix bundle passed, verify:

- The `.tex` file is standalone and starts with Appendix, not body text.
- Included artifacts are audited official evidence unless explicitly labeled validation appendix.
- Every table and figure has a caption/title and notes.
- Notes match source specs, logs, table plan, and figure inventory.
- Displayed variable labels satisfy the one-word/default and two-word/maximum rule.
- Notes explain represented constructs and proxy status for dependent and key explanatory variables.
- Appendix Table A is present and valid when empirical variables appear in the appendix bundle, unless an approved exception is recorded.
- No Python cross-check or `validation_cross_check_evidence` artifact is included as official evidence.
- LaTeX compiles with XeLaTeX or, if LaTeX is unavailable, the environment blocker is recorded and static structure checks pass.
- Any LaTeX syntax error in the generated `.tex` is a P0 blocker unless caused solely by missing local LaTeX tooling.

## forbidden_actions
- Do not write manuscript body text, results prose, causal conclusions, policy implications, or contribution claims.
- Do not include Introduction, Results, Robustness, Mechanism, Conclusion, or reference-section body content.
- Do not manually edit or enter coefficients, standard errors, p-values, stars, sample sizes, or figure values.
- Do not include unaudited, blocked, failed, pending, or cross-check artifacts as official appendix evidence.
- Do not include any table or figure without notes.
- Do not use long variable labels in final table bodies, column headers, figure axes, legends, or captions.

## P0_risks
- Appendix `.tex` contains manuscript body text.
- Appendix includes validation/cross-check artifacts as official evidence.
- A table or figure lacks notes.
- A final display label for a variable exceeds two words.
- Appendix Table A is missing or malformed when empirical variables appear and no approved exception is recorded.
- Regression table notes omit the represented construct or proxy status for dependent variable(s) or key explanatory variable(s), or use only Y/X names without meaning.
- Notes invent unsupported model/sample/variable details or contain causal conclusions.
- Generated `.tex` fails to compile due to structure or syntax errors.

## evidence_requirements
Appendix artifacts require passed source audits, source scripts/logs, generated outputs, notes, and compile/static LaTeX checks. The Appendix bundle itself is verified evidence only after its source links and notes pass audit.
