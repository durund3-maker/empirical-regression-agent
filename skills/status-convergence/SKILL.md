---
name: status-convergence
description: Check review and handoff status files for contradictions before marking an empirical package complete or transferring it downstream.
---

# status-convergence

## description
Use this skill immediately before final handoff status. It verifies that P0/P1/P2, approval, bundle, transfer, proposal/executed/final, and TODO statuses are consistent across review files and handoff manifests.

## required_inputs
- Project `review/` records.
- `handoff_package/` records, if already created.
- Handoff manifest and evidence map, if present.

## required_outputs
- `review/status_convergence_report.md`
- Blocking Stop Message when conflicts remain.

## workflow
1. Run `scripts/status_convergence_check.py --project-root <project> --output review/status_convergence_report.md --fail-on-conflict` when available.
2. Inspect any complete/pending, complete/not-built, approved/not-approved, proposal/final, or transfer-approved/not-approved conflicts.
3. Inspect handoff manifests for `pending`, `proposal`, `not_executed`, `unverified`, or `not approved` materials.
4. If conflicts exist, mark handoff as blocked and do not transfer to `empirical-paper-agent`.
5. If no conflicts exist, record that status convergence passed but does not replace regression, table, encoding, or replay audits.

## P0_risks
- Handoff audit says complete while another review file says a required bundle or gate remains pending.
- Proposal-only or unapproved files are included in final handoff.
- Transfer status is not separately approved.

