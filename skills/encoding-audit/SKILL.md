---
name: encoding-audit
description: Audit Markdown, CSV, YAML, TXT, TEX, DO, and Python outputs for UTF-8 readability and mojibake before final handoff.
---

# encoding-audit

## description
Use this skill before final handoff and whenever Chinese text appears in generated files. It prevents mojibake-damaged artifacts from entering final bundles or handoff packages.

## output_policy
- Markdown, YAML, TXT, Python, Stata do files, and internal CSV outputs default to `encoding="utf-8"`.
- Final CSV files intended for Excel opening may use `encoding="utf-8-sig"` when documented in the audit.
- Stata exports with Chinese text must document the export encoding strategy and must pass a post-export readability check.

## workflow
1. Run `scripts/encoding_check.py --root <project> --output review/encoding_audit.md --fail-on-finding` or scan the intended handoff paths.
2. Treat UTF-8 decode errors, replacement characters, `???`, or common mojibake sequences as blocking findings.
3. Correct or exclude damaged files before handoff.
4. Record encoding policy, scanned files, findings, and final decision.

## P0_risks
- Mojibake appears in a variable dictionary, audit report, handoff README, evidence map, or any final packaged text artifact.
- A file cannot be decoded as UTF-8/UTF-8-SIG.
- Damaged text is included in handoff without exclusion or correction.

