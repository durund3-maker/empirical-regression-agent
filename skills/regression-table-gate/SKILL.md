---
name: regression-table-gate
description: Apply hard gates to regression tables before manuscript-ready bundle or handoff main-evidence inclusion.
---

# regression-table-gate

## description
Use this skill after regression table export and before table bundle construction or handoff. It classifies pathological regression tables as blocked from main evidence.

## workflow
1. Run `scripts/regression_table_gate.py --table <table.csv> --log-file <stata.log> --output review/regression_table_gate.md`.
2. Use default candidate thresholds unless an approved project config overrides them: `min_n=30`, `r2_near_one_threshold=0.995`, `min_obs_per_parameter=5`, and unexplained sample loss above 50%.
3. If the status is `BLOCK_MAIN_BUNDLE`, mark the table as appendix diagnostic or excluded.
4. Record the downgrade reason in `review/table_output_audit.md` and bundle build reports.

## P0_risks
- A hard-gated table enters `Tables and Figures`.
- A hard-gated table enters handoff main evidence.
- Audit files do not explain why a table was downgraded or excluded.

