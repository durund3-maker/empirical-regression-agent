# Empirical Regression Agent

Empirical Regression Agent is a reproducible execution and audit framework for empirical regression projects. It scaffolds projects, proposes auditable empirical workflows, runs approved Stata-oriented analysis steps, validates logs and tables, and prepares handoff packages.

It is not a manuscript-writing agent. It produces traceable empirical artifacts for later use by a researcher or a paper-writing agent.

## What It Does

- Initializes regression project folders and rule files.
- Audits data inventories, variable dictionaries, sample flows, and evidence maps.
- Proposes identification, cleaning, variable construction, descriptive statistics, baseline, event-study, robustness, and mechanism workflows.
- Runs approved Stata commands through auditable wrappers.
- Parses logs, validates tables, and builds handoff packages.

## What It Does Not Do

- It does not choose the final identification strategy for the researcher.
- It does not adjust models to obtain statistical significance.
- It does not invent data, variables, coefficients, p-values, tables, or causal claims.
- It does not write manuscript body text.

## Repository Layout

- `AGENTS.md`: Scope, boundaries, evidence rules, and human checkpoints.
- `WORKFLOW.md`: Productized empirical workflow.
- `agent_core/`: Core evidence, gate, Stata, table, and handoff rules.
- `config/`: Fillable schemas for project metadata and audit records.
- `skills/`: Reusable workflow modules.
- `agents/`: Specialized role prompts.
- `templates/`: Project, Stata, report, inventory, and handoff templates.
- `scripts/`: Local CLI utilities.
- `tests/`: Unit tests for scripts and gates.
- `docs/`: Operator and attribution notes.

## Setup

The core scripts use the Python standard library. For local validation, install pytest:

```bash
python -m pip install pytest
```

## Quick Start

```bash
python scripts/project_initializer.py --project-name demo --project-root projects --template-dir templates --project-title "Demo Project" --main-data "data.csv" --research-question "X affects Y"
```

Add `--execute` only after confirming the scaffold plan.

## Test

```bash
python -m pytest
```

## Safety Notes

Do not commit raw or processed data, logs, generated regression outputs, private handoff packages, or local Stata paths. Keep project-specific artifacts in ignored `projects/<name>/` subdirectories unless they have been explicitly sanitized.
