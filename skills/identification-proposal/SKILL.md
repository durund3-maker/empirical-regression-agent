---
name: identification-proposal
description: Propose feasible empirical identification strategies from the research question, metadata, and safe data inspection before any regression execution. Use when a project needs candidate Y/X/unit/time/proxy variables, an identification-tree path, method-card references, and researcher approval.
---

# identification-proposal

## name
identification-proposal

## description
Use this skill after project bootstrap and initial inventory to prepare an identification-strategy proposal. The skill reads project metadata, dictionaries, author notes, safe data previews, and method cards under `references/method-cards/`. It recommends feasible and infeasible design families for researcher review, but it does not decide identification validity or execute empirical models.

## required_inputs
- `PROJECT_RULES.md` or `config/project_metadata.yml`.
- Research question, main data path, and software environment.
- Data dictionary, variable labels, safe column previews, or inventory reports where available.
- Method cards such as DID, modern DID, IV, RDD, synthetic control, matching/DML, and shift-share.

## required_outputs
- `review/identification_strategy_proposal.md`
- Optional `review/identification_risk_register.md`
- Pending researcher decision entry in the project gate status.

## output_language
Researcher-facing Markdown prose in the proposal and risk register should be written in Chinese whenever practical. Preserve variables, formulas, field names, code, file paths, commands, Stata package names, model names, schema values, evidence-class labels, decision enums, and machine-readable blocks in their original form.

## workflow
1. Parse the research question into candidate outcome, treatment/key explanatory variable, unit, time, and plausible proxy variables.
2. Inspect only approved metadata, dictionaries, labels, and safe previews; do not clean data or run regressions.
3. Walk the identification tree: treatment assignment known, identification source, timing structure, shock/tool/cutoff/control availability, and observables-only alternatives.
4. List feasible designs, infeasible designs, missing evidence, diagnostic commands, and method-card references.
5. Classify each claim as `author decision`, `agent inference`, `open risk`, or `unverified claim`.
6. Stop for researcher approval of the design family before regression specs or event-study windows are locked.

## forbidden_actions
- Do not execute regressions or descriptive-result tables.
- Do not claim that identification is valid.
- Do not label an event or policy as exogenous without documented evidence and approval.
- Do not choose a design because preliminary estimates are significant.
- Do not write manuscript causal conclusions or mechanism claims.

## human_review_checkpoint
Researcher confirmation is required for the selected identification strategy, treatment assignment rule, key proxy variables, control group concept, event window concept, and whether the design may support causal language.

## P0_risks
- Treatment assignment mechanism is unclear.
- Candidate outcome, treatment, unit, or time cannot be mapped to documented variables.
- Formal causal identification language appears without approval and evidence.
- The proposal relies on agent inference as verified evidence.

## P1_risks
- Proxy variables are weak or indirect.
- Identification depends on unverified timing, cutoff, shock, or donor-pool assumptions.
- Data support is sparse for pre-trend, first-stage, density, balance, or placebo diagnostics.

## evidence_requirements
Every design recommendation must cite a metadata field, data dictionary item, author note, observed variable inventory, or method card. Unsupported assumptions remain open risks.
