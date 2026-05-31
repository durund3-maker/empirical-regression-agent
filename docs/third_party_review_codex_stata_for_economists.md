# Third-Party Review: codex-stata-for-economists

## External Repository Positioning

Reviewed repository: `maxwell2732/codex-stata-for-economists`  
URL: https://github.com/maxwell2732/codex-stata-for-economists

This external repository is a Stata empirical research workflow template. Its center of gravity is a concrete Stata project layout: `dofiles/00_master.do` as the pipeline entry point, `dofiles/01_clean/` through `04_output/` as executable stages, `scripts/run_stata.sh` and `scripts/run_pipeline.sh` as shell wrappers, data safety checks, quality scoring, Quarto reporting, and Claude/Codex operating rules.

For the current `empirical-regression-agent`, it should be treated only as third-party reference material. The current repository is a reusable execution and audit framework, not a concrete Stata project template and not a manuscript-writing agent. Current `AGENTS.md`, `WORKFLOW.md`, `agent_core/`, and `config/` remain superior rules.

## Relationship to Empirical-Regression-Agent

Useful alignment:

- Strong "no log, no claim" discipline maps well to current evidence grounding rules.
- Data-protection rules reinforce current raw-data read-only and no-leak requirements.
- Stata reproducibility rules support current requirements for complete logs, explicit run order, and traceable outputs.
- The shell wrapper and data-safety script are useful design references for future execution tooling.
- The quality scoring script is useful as a static-check concept, but its scoring rubric must be adapted to P0/P1/P2 gates.

Important boundary differences:

- The external repository is structured as a concrete project scaffold with `dofiles/`, `data/`, `output/`, `reports/`, and `explorations/`; this current stage must not create a concrete project.
- The external repository includes report and paper-oriented Quarto prose sections; the current agent must not write manuscript body text or causal conclusions.
- The external repository includes Claude skills and commands such as `/lit-review`, `/review-paper`, and `/research-ideation`; these are outside the current regression-agent boundary.
- The external repository includes hardcoded local environment examples, including Stata and Python paths and version guidance; those cannot be imported as framework defaults.
- The external Stata templates include example analysis calls and package installation recipes; those cannot be ported directly because this round must not create Stata regression code.

## Reviewed External Materials

The audit reviewed or attempted to review the following materials through GitHub file reads because direct `git clone` failed due network connection failure:

- `AGENTS.md`
- `CLAUDE.md`
- `.claude/skills/stata/SKILL.md`
- `.claude/rules/log-verification-protocol.md`
- `.claude/rules/data-protection.md`
- `.claude/rules/stata-reproducibility-protocol.md`
- `.gitignore`
- `scripts/run_stata.sh`
- `scripts/run_pipeline.sh`
- `scripts/check_data_safety.py`
- `scripts/quality_score.py`
- `dofiles/00_master.do`
- `templates/master-do-template.do`
- `reports/analysis_report.qmd`
- `reports/_quarto.yml`

Directory-level review of `dofiles/01_clean/`, `02_construct/`, `03_analysis/`, and `04_output/` found the repository's documented structure and commented placeholders in `00_master.do`, but no project-specific executable files were imported into this repository.

## Borrowable Ideas

Directly useful as design principles:

- Treat logs and exported tables as mandatory evidence before any numerical claim.
- Refuse to state results when the relevant do-file has not been run or the log is stale or missing.
- Keep raw and derived data out of version control using both `.gitignore` and an explicit staged-file checker.
- Separate pipeline execution from report rendering; reports should consume generated outputs rather than generate empirical results.
- Capture Stata environment snapshots and package availability in logs.
- Use wrapper scripts that propagate Stata exit codes and expose log tails on failure.
- Use static quality checks to catch missing `version`, missing `log using`, hardcoded paths, absent seeds where randomness appears, and report chunks that contain analysis commands.

Useful only after adaptation:

- `scripts/run_stata.sh`: adapt to Windows and cross-platform Stata discovery, project metadata, and current log naming rules.
- `scripts/run_pipeline.sh`: adapt from concrete `dofiles/00_master.do` execution to project-workspace run manifests.
- `scripts/check_data_safety.py`: adapt to this framework's project directory conventions and confidentiality metadata.
- `scripts/quality_score.py`: replace the external 80/90/95 score gate with current P0/P1/P2 taxonomy.
- `dofiles/00_master.do` and `templates/master-do-template.do`: use only as reference for future template design, not as code to import now.
- `.claude/skills/stata/SKILL.md`: use its gotcha list and routing design as future skill inspiration, not as a direct skill import.

## Not Directly Importable

The following should not be directly introduced into this repository:

- `CLAUDE.md` as an instruction file, because this repo already has a stricter agent identity and scope.
- Claude slash-command lists, manuscript review commands, literature review commands, or ideation commands.
- Quarto manuscript/report prose scaffolds with Introduction, Identification, Results, and Conclusion sections.
- Example Stata regression commands, event-study snippets, DiD snippets, graph examples, or cleaning examples as executable code.
- Hardcoded local paths such as machine-specific Stata or Miniconda locations.
- Fixed Stata version requirements such as Stata 15 or 17 as global framework defaults.
- Any external file copied verbatim before license status is clarified.

## Conflicts With Current Superior Rules

- Manuscript-writing conflict: the external Quarto report template contains narrative paper sections and prompts for empirical interpretation. Current rules prohibit manuscript body prose and unsupported causal conclusions.
- Checkpoint conflict: external templates imply an executable project scaffold. Current rules require researcher confirmation before sample rules, merge keys, variable formulas, fixed effects, clustering, controls, event-study windows, robustness matrices, heterogeneity/mechanism designs, and final table order.
- Gating conflict: external quality scores use 80/90/95 thresholds. Current framework uses P0/P1/P2 risk taxonomy where P0 blockers cannot be averaged away by a high score.
- Environment conflict: external instructions include author-machine paths and version assumptions. Current framework must keep project environments configurable and auditable.
- Scope conflict: external skills include literature review, proofread, paper review, and research ideation. Current framework is not `empirical-paper-agent`.
- Code-generation conflict: external Stata examples could become unapproved regression code if copied. This round explicitly prohibits creating Stata regression code.

## Recommended Absorption Order

1. Reference documentation: record external repo and license/attribution status before any future reuse.
2. Data safety design: adapt the staged-file checker concept into a framework script after project path conventions are finalized.
3. Log verification protocol: convert "no log, no claim" into audit checklist language and skill behavior for log review.
4. Stata run wrapper design: later build a cross-platform wrapper that reads project metadata rather than hardcoding paths or version.
5. Quality checks: map static checks to P0/P1/P2 findings instead of a numeric score.
6. Stata skill material: selectively transform gotchas into future skill guidance, with attribution if expressive text or examples are adapted.
7. Templates: only after the template phase, create original framework templates that enforce checkpoints and contain placeholders rather than concrete variables or regression commands.
