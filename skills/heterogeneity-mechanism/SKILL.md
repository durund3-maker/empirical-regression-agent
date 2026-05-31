---
name: heterogeneity-mechanism
description: Run and audit approved heterogeneity, mechanism-related, moderation, or mediation regressions while keeping evidence classes separate. Use when subgroup or channel designs need regression-ready outputs, caution flags, and no manuscript claims.
---

# heterogeneity-mechanism

## name
heterogeneity-mechanism

## description
Use this skill to run and audit approved heterogeneity, mechanism-related, moderation, or mediation regression workflows while keeping those evidence classes separate. Heterogeneity does not equal mechanism unless the researcher explicitly defines and documents that design. This skill outputs regression-ready evidence, risk flags, and caution notes, not manuscript prose.

## when_to_use
Use after baseline specifications and subgroup or mechanism-related designs are approved when the user asks to run, classify, or audit heterogeneity or mechanism-related empirical outputs.

## required_inputs
- Approved heterogeneity or mechanism-related design.
- Subgroup definitions, moderation or mediation definitions, and mechanism-related variable documentation.
- Approved analysis data, variable dictionary, sample-flow records, and baseline links.
- Expected output plan and evidence-class requirements.

## required_outputs
- `output/tables/heterogeneity_*.*`
- `output/tables/mechanism_related_*.*`
- `review/heterogeneity_mechanism_audit.md`
- `review/mechanism_caution_flags.md`

## workflow
1. Classify each requested design as heterogeneity, mechanism-related, moderation, mediation, or other documented category.
2. Verify researcher approval for subgroup definitions, mechanism-related variables, sample, FE, cluster, controls, estimator, and output labels.
3. Execute only approved models and maintain explicit spec IDs, FE, clustering, controls, sample filters, and logs.
4. Export tables through executable code; do not manually fill numbers.
5. Assign evidence class to each output: verified evidence, author decision, agent inference, open risk, or unverified claim.
6. Flag proxy-based, indirect, weak, or overstatement-prone mechanism-related evidence as P1 when not blocking.
7. Write audit and caution files without manuscript claims or causal mechanism conclusions.

## forbidden_actions
- Do not treat heterogeneity as mechanism by default.
- Do not write manuscript body text or causal conclusions.
- Do not invent channel variables, subgroup definitions, mediation paths, or mechanism interpretations.
- Do not change specifications to obtain significance.
- Do not present agent inference as verified evidence.

## human_review_checkpoint
Researcher confirmation is required for subgroup definitions, mechanism-related variables, moderation or mediation design, evidence labels, FE, clustering, controls, sample, estimator, and final output labels.

## P0_risks
- Heterogeneity or mechanism-related design is unapproved.
- Mechanism-related variable is undocumented.
- Output lacks log, spec link, or audit record.
- Agent inference is presented as verified evidence.

## P1_risks
- Mechanism-related evidence is proxy-based, indirect, or weak.
- Heterogeneity evidence may be overstated as mechanism downstream.
- Subgroup sizes or sample shifts affect interpretation.

## expected_files
- `output/tables/heterogeneity_*.*`
- `output/tables/mechanism_related_*.*`
- Logs for executed models.
- `review/heterogeneity_mechanism_audit.md`
- `review/mechanism_caution_flags.md`
- Failure record for failed models.

## evidence_requirements
Each result must link to approved design, executable code, complete log, exported table, and audit status. Mechanism-related outputs must explicitly state evidence class. No log, no claim.

## audit_trail_requirements
Record design class, approval references, spec IDs, scripts, logs, outputs, failures, evidence class, caution flags, and P0/P1/P2 status.
