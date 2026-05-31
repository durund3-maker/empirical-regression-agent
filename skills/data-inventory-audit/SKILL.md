---
name: data-inventory-audit
description: Audit raw data inventory, data paths, file formats, keys, time variables, sample coverage, Git exposure, and data safety risks. Use before cleaning or variable construction when Codex must inspect data availability and risks without modifying data.
---

# data-inventory-audit

## name
data-inventory-audit

## description
Use this skill to audit raw data inventory, file paths, formats, keys, time variables, sample periods, Git exposure, and data safety risks. This skill is read-only: it reports data availability, structure, leakage, privacy, and authorization issues without cleaning, deleting, recoding, or overwriting data.

## when_to_use
Use after project intake when the user asks to inspect raw data coverage, check whether files are safe and traceable, or audit data availability before cleaning or variable construction.

## required_inputs
- `output/material_map.md` or equivalent material inventory.
- Project metadata, data-source list, data dictionary, and author notes if available.
- Raw-data paths and any documented access or confidentiality restrictions.
- Git status or repository file listing for checking accidental raw-data inclusion.

## required_outputs
- `review/data_inventory_audit.md`
- `output/data_file_inventory.csv`
- `review/data_safety_risks.md`

## workflow
1. Read the material map and metadata to identify declared raw and derived data files.
2. Verify whether declared data files exist, are readable, and match documented formats.
3. Inspect structure only as allowed: variable names, row counts, file format, keys, time variables, sample period, and missingness summaries.
4. Check key uniqueness with non-destructive methods and record whether `isid`, duplicate reports, or equivalent checks are needed.
5. Check whether raw or sensitive data are tracked by Git or placed in inappropriate output locations.
6. Identify data leakage, privacy, license, or authorization risks from metadata and observed paths.
7. Write `data_file_inventory.csv` with stable paths, roles, formats, key fields, time fields, sample coverage, and evidence class.
8. Write audit and safety-risk reports with P0/P1/P2 classifications.

## forbidden_actions
- Do not clean, delete, move, rewrite, subset, deduplicate, merge, or recode data.
- Do not modify raw data or create new empirical results.
- Do not infer undocumented variables as usable regression inputs.
- Do not suppress data safety risks for convenience.

## human_review_checkpoint
Researcher confirmation is required for ambiguous file roles, unclear provenance, uncertain authorization, undocumented keys, and any decision about how to handle safety or leakage risks.

## P0_risks
- Raw data are modified or placed under generated-output control.
- Core data files are unreadable or missing.
- Data safety or authorization issue blocks use.
- Required keys or time variables are absent and no approved alternative exists.

## P1_risks
- Key uniqueness or missingness may affect planned specifications.
- Sample period differs from metadata.
- Provenance is incomplete but not blocking immediate inventory.
- Sensitive fields require special handling before execution.

## expected_files
- `output/material_map.md`
- `output/data_file_inventory.csv`
- `review/data_inventory_audit.md`
- `review/data_safety_risks.md`

## evidence_requirements
Each audit finding must cite a data path, metadata field, data dictionary entry, Git listing, or author note. Observed structure is `agent inference` until linked to approved metadata or passed audit.

## audit_trail_requirements
Record files inspected, checks performed, whether raw data were read-only, Git inclusion status, unresolved data questions, and safety-risk severity.
