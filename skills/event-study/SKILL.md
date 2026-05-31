---
name: event-study
description: Execute approved event-study, dynamic-effect, and pre-trend workflows with documented windows, omitted periods, binning, lead/lag construction, logs, tables, figures, and failure records. Use only after the event-study design is confirmed.
---

# event-study

## name
event-study

## description
Use this skill to generate and execute approved dynamic-effect, event-study, and pre-trend workflows. It requires documented event window, omitted period, binning rule, and lead/lag construction, and it prevents unsupported claims that insignificant pre-trends prove identification.

## when_to_use
Use after baseline specifications and event-study design choices are confirmed when the user asks to run dynamic effects, pre-trend checks, coefficient tables, or event-study figures.

## required_inputs
- Approved event-study specification or design note.
- Confirmed event window, omitted period, binning rule, and lead/lag construction.
- Approved analysis data, variable dictionary, and sample-flow records.
- Baseline linkage and expected table or figure plan.

## required_outputs
- `output/tables/event_study.*`
- `output/figures/event_study.*`
- `output/logs/event_study.log`
- `review/event_study_audit.md`

## workflow
1. Confirm researcher approval for event window, omitted period, binning, lead/lag construction, fixed effects, clustering, controls, and sample.
2. Generate or execute event-study code with complete Stata setup and logs.
3. Log event-time construction, sparse bins, collapsed tails, omitted period, and sample counts.
4. Run only approved event-study models and export coefficient tables and figures through executable code.
5. Ensure figures are generated from stored coefficients or reproducible graph commands.
6. Record failed or blocked event-study models in the failure record with spec ID, script, log, error, and next action.
7. Write `event_study_audit.md` with evidence links, P0/P1/P2 risks, and caution notes.

## forbidden_actions
- Do not change event window, omitted period, binning, FE, cluster, controls, or sample without approval.
- Do not suppress unfavorable or sparse periods without documentation.
- Do not interpret pre-trend insignificance as proof that identification fully holds.
- Do not hand-fill event-study estimates or figure data.
- Do not write mechanism or causal manuscript conclusions.

## human_review_checkpoint
Researcher confirmation is required for event window, omitted period, binning rule, lead/lag construction, fixed effects, clustering, controls, sample, and figure/table order.

## P0_risks
- Event window or omitted period is unclear or unapproved.
- Event-time construction is undocumented.
- Required log or figure/table source is missing.
- Failed event-study model is omitted from failure records.

## P1_risks
- Sparse event-time cells affect interpretation.
- Window or binning choices are sensitive.
- Pre-trend evidence is likely to be overstated downstream.

## expected_files
- `output/tables/event_study.*`
- `output/figures/event_study.*`
- `output/logs/event_study.log`
- `review/event_study_audit.md`
- Failure record if any model fails.

## evidence_requirements
Event-study claims require approved design, executable code, complete log, exported table or figure, and audit status. No log, no claim.

## audit_trail_requirements
Record design approvals, event-time construction, omitted period, window, binning, scripts, logs, outputs, failures, and evidence class for each output.
