## v0.1 candidate - 2026-05-28

### Source
Based on the `price_and_design` workflow review.

### Fixed
- Added a hard gate for pathological regression tables before manuscript-ready bundle and handoff main-evidence inclusion.
- Added final status convergence checks before handoff completion or transfer.
- Split proposal, executed, and handoff variable dictionary semantics.
- Added encoding integrity checks for UTF-8 readability and mojibake before handoff.
- Improved Windows Stata local batch path handling with `cd /d`, quoted paths, relative do-file paths, command preview, and command log.
- Improved Stata log parser classification so echoed `display as error` code is not automatically treated as a real P0 execution error.
- Added itemized HITL approval requirements for high-risk operations that cannot be cleared by generalized approval.
- Added questionnaire codebook audit requirements before strong-meaning variable construction.
- Added mandatory HITL review indexes for approval gates, including pre-execution review indexes with Markdown links and full relative paths.
- Required Markdown review versions for identification summary, pre-execution plan, data processing rules, variable construction, sample rules, estimator/SE plan, table/figure plan, risk statement, and approval checklist.
- Required HITL gate final replies to list review index and key files with links, paths, descriptions, and decisions needed.
- Added Tables/Figures layout rules for centered notes, decimal precision, main-table page breaks, centered Appendix placement, duplicate table-number prevention, and format audits.
- Added handoff blocking rule for combined Tables/Figures bundles with unresolved format-audit failures.

### Added
- `skills/regression-table-gate/SKILL.md`
- `skills/status-convergence/SKILL.md`
- `skills/encoding-audit/SKILL.md`
- `skills/questionnaire-codebook-audit/SKILL.md`
- `skills/hitl-review/SKILL.md`
- `skills/tables-figures-format/SKILL.md`
- `scripts/regression_table_gate.py`
- `scripts/status_convergence_check.py`
- `scripts/encoding_check.py`
- `scripts/tables_figures_format_check.py`
- Separate proposal, executed, and handoff variable dictionary templates.
- `templates/HITL_REVIEW_INDEX.md`
- `templates/pre_execution_approval_checklist.md`
- `templates/table_note_block.tex`
- `templates/tables_figures_layout.tex`
- Focused tests for Stata log parsing, regression table gating, status convergence, encoding audit, and Tables/Figures format audit.
- `tests/test_tables_figures_format_check.py`

### Supplemental fixes from human review
- HITL review index is required at every HITL approval gate.
- Critical approval files must have Markdown review versions.
- HITL gate replies must include Markdown link plus full relative path.
- Table/figure notes must be centered or placed in centered table note systems.
- Descriptive statistics and model-output decimals must be normalized before final export.
- Table 2 and later main tables must start on a new page unless compact output is explicitly approved.
- Appendix must appear after the last main artifact, with a preceding page break and centered title.
- Duplicate `Table.x:` captions are forbidden.
- Tables/Figures format audit is required before final/PDF/handoff status.

### Not fixed
- Existing historical mojibake in old framework review files was not globally repaired.
- Existing `price_and_design` project outputs were not rewritten.
- The full empirical workflow was not rerun.

### Validation status
- `v0.1 candidate generated`
- `not stable yet`
- `requires fresh workflow validation`
