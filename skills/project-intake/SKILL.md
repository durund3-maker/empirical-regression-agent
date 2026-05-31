---
name: project-intake
description: Start an empirical-regression project intake by reading project metadata, inventorying supplied materials, and producing material, variable, table-plan, and missing-information maps. Use before any cleaning, regression, table interpretation, or handoff work.
---

# project-intake

## name
project-intake

## description
Use this skill to start a concrete empirical-regression project by reading `project_metadata.yml`, inventorying the provided `data/`, `code/`, `output/`, and `review/` folders, and creating the first material, variable, table, and missing-information maps. This skill establishes project boundaries and evidence gaps; it does not clean data, run regressions, or create result interpretations.

## when_to_use
Use when a project workspace already exists and the user asks to begin intake, map supplied empirical materials, verify initial project metadata, or identify missing inputs before any empirical execution.

## required_inputs
- `project_metadata.yml` or a clearly marked missing metadata gap.
- Existing `data/`, `code/`, `output/`, and `review/` directories when available.
- Author notes, expected empirical outputs, software requirements, and data-source list if provided.
- Top-level rules from `AGENTS.md`, `WORKFLOW.md`, `agent_core/`, and `config/`.

## required_outputs
- `output/material_map.md`
- `output/variable_map.csv`
- `output/table_plan.csv`
- `review/missing_info.md`
- `review/project_intake_report.md`

## workflow
1. Read project metadata and classify missing fields as `needs_author_input`, `explicitly_unavailable`, or `not_applicable`.
2. Inventory `data/`, `code/`, `output/`, and `review/` without modifying raw or derived materials.
3. Classify artifacts by observed role: raw input, derived input, executable script, log, table, figure, author note, audit record, or unknown.
4. Draft `material_map.md` with file paths, observed provenance, role, evidence class, and open questions.
5. Draft `variable_map.csv` as an intake-level map only; do not invent formulas, units, or labels.
6. Draft `table_plan.csv` from documented expected outputs only; mark unsupported table expectations as missing.
7. Write `missing_info.md` with P0/P1/P2 risk labels.
8. Write `project_intake_report.md` summarizing what was inspected, what was produced, and what remains blocked.

## forbidden_actions
- Do not create a concrete project if none exists.
- Do not run data cleaning, variable construction, descriptive statistics, or regressions.
- Do not invent data sources, variable names, formulas, table rows, coefficients, sample sizes, or interpretations.
- Do not treat file-name guesses as verified evidence.
- Do not write manuscript prose or causal conclusions.

## human_review_checkpoint
Researcher confirmation is required for project scope, owner, data locations, confidentiality constraints, expected output list, and whether missing inputs are genuinely unavailable.

## P0_risks
- Missing project owner, output scope, or raw-data location.
- Core input directories or metadata cannot be located and are not explicitly marked unavailable.
- Raw data appear modified during intake.
- Intake maps present agent inference as verified evidence.

## P1_risks
- Software versions, package requirements, or runtime expectations are uncertain.
- File provenance is incomplete for non-core artifacts.
- Expected tables or variables are mentioned in notes but not supported by metadata.

## expected_files
- `project_metadata.yml`
- `data/`
- `code/`
- `output/`
- `review/`
- `output/material_map.md`
- `output/variable_map.csv`
- `output/table_plan.csv`
- `review/missing_info.md`
- `review/project_intake_report.md`

## evidence_requirements
Every intake claim must cite a path, metadata field, author note, or observed directory state. Claims based on names or layout must be labeled `agent inference`. Missing information must be recorded as a gap, not filled.

## audit_trail_requirements
Record inspection date, inspected directories, generated files, missing required inputs, P0/P1/P2 status, and all author confirmations required before later stages.
