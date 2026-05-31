# Evidence Rules

Every result, status claim, or audit finding must be grounded in traceable artifacts. Missing evidence must be reported as a gap, not filled by inference.

## Evidence Classes

## Verified Evidence

Verified evidence is a claim supported by a complete artifact chain:

1. Researcher-approved input or documented source.
2. Executable script or do file.
3. Complete execution log.
4. Exported table, figure, dataset, or inventory.
5. Audit record with status `passed`.

Only verified evidence may support final empirical status claims.

## Author Decision

An author decision is a researcher-provided choice or approval, such as:

- Sample rule.
- Merge key.
- Variable formula.
- Fixed effects.
- Clustering level.
- Controls.
- Event-study window and omitted period.
- Robustness matrix.
- Final table order.

Author decisions must be preserved as notes or config entries. They are valid inputs but are not empirical results by themselves.

## Agent Inference

Agent inference is a bounded conclusion from file names, paths, logs, manifests, schemas, or directly observed code. It must be labeled as inference and cannot be upgraded to verified evidence until audited.

Examples:

- Inferring that a table is linked to a do file because of matching names.
- Inferring that a log belongs to a run because of timestamps.
- Inferring project structure from directory layout.

## Open Risk

An open risk is a documented uncertainty that may affect execution, interpretation, or handoff. Open risks must be classified as P0, P1, or P2.

Examples:

- Missing log for a non-core robustness table.
- Unclear sample difference between baseline and robustness.
- Mechanism-related variable is proxy-based.

## Unverified Claim

An unverified claim is any claim that lacks a complete evidence chain or researcher decision. It must not be used as an empirical result.

Examples:

- "The baseline result is significant" without a log and table.
- "The mechanism is confirmed" from a heterogeneity table.
- "The sample drop is acceptable" without approved sample rules.

## Accepted Artifacts

Accepted evidence artifacts include:

- Source do files or executable scripts.
- Complete execution logs.
- Exported tables.
- Exported figures.
- Data dictionaries and variable maps.
- Project metadata.
- Author notes and approvals.
- Reproduction manifests.
- Audit status records.
- Sample-flow records.

## Non-Evidence

The following are not sufficient by themselves:

- Memory of prior runs.
- Unlogged console output.
- Screenshots without source files.
- Informal summaries.
- Expected signs or expected significance.
- Researcher preferences not recorded in notes or config.
- Agent assumptions.
- Manually edited table values.

## Evidence Gap Procedure

When evidence is missing, the agent must:

1. Name the missing artifact.
2. Identify affected outputs or claims.
3. Classify severity as P0, P1, or P2.
4. Avoid filling the gap with inference.
5. Request author input or execute approved scripts when appropriate.
6. Record the gap in audit status and risk reports.

## Reviewer and Audit Boundary

Reviewers and audit agents may:

- Inspect artifacts.
- Compare specs, scripts, logs, tables, figures, and inventories.
- Classify evidence and risks.
- Record findings and remediation requirements.

Reviewers and audit agents must not:

- Edit numerical results.
- Change sample rules, variable formulas, fixed effects, clustering, controls, or estimators.
- Change table values, stars, or model labels to make outputs look consistent.
- Convert failed, blocked, or unaudited outputs into passed outputs without evidence.
- Rewrite empirical conclusions or mechanism claims.
