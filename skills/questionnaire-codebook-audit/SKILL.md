---
name: questionnaire-codebook-audit
description: Audit questionnaire codebooks before variable construction, especially Likert, multi-select, cascade, matrix, and coded-option fields.
---

# questionnaire-codebook-audit

## description
Use this skill before constructing variables from survey or questionnaire data. It determines whether codes are real quantities/time or option labels, and whether variables can be used in indexes, regressions, or only descriptive outputs.

## required_checks
- Question type: single choice, multiple choice, matrix, cascade, open text, numeric, date/time, or unknown.
- Whether coded values represent real quantities/time or only option order.
- Likert direction and whether reverse coding is required.
- Missing-value meaning.
- Multi-select semantics: unchecked, missing, not displayed, or skipped.
- Whether sum, mean, index, or factor construction is allowed.
- Skip logic, branching, and display conditions.
- Original question number, code meaning, direction, missing meaning, and index eligibility.

## workflow
1. Inspect the codebook or data dictionary before variable construction.
2. Write codebook-audit findings into the variable-construction proposal.
3. If a field is ambiguous, allow only `proposal_variable_dictionary.csv` or descriptive-only use.
4. Require itemized HITL approval before using ambiguous codes for strong-meaning variables, indexes, or timing.

## P0_risks
- Cascade option codes are treated as real month/year/time values without evidence.
- Likert or index direction is unknown but used in regression.
- Multi-select missingness is unknown but used as a substantive zero.

