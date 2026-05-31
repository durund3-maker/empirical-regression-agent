---
name: pipeline-orchestrator
description: Run an empirical project through the productized regression-agent workflow until the next required researcher approval gate. It coordinates bootstrap, intake, identification proposals, data-processing proposals, regression execution, audit, revision, cleanup, commits, and handoff while stopping only for P0 risks or explicit researcher approval.
---

# pipeline-orchestrator

## name
pipeline-orchestrator

## description
Use this total-control skill to run `empirical-regression-agent` in a run-to-gate productized mode. It does not replace the existing project, identification, data, variable, regression, audit, table, or handoff skills. It schedules them, checks gates, records status, and keeps moving through low-risk work until it reaches either a P0 blocker, an explicit researcher approval gate, a researcher request for manual review, or final handoff completion.

The skill reduces manual interruptions, but it does not remove researcher approval. A recommended plan is not approval. Researcher silence is not approval. Formal causal identification P0 cannot be cleared by this skill.

## modes

### Mode 1: PLAN_AUTOPILOT
Use after the researcher provides a project topic and data location, before execution approval exists.

Automatically complete:

1. AEA/DCAS-style project bootstrap when a project workspace is authorized.
2. Raw data safety check.
3. Limited intake.
4. Method-card and variable dictionary preparation.
5. Identification-strategy proposal and identification-tree path.
6. Data-processing proposal covering unit, time, keys, deduplication, sample, missing, outliers, formulas, event windows, multiple treatment, and control-group rules.
7. Pre-execution proposal.
8. Proposal package commit, only if autopilot commit is explicitly allowed and commit safety checks pass.

Then stop for researcher approval.

Do not read raw data beyond safety/inventory checks authorized by the relevant intake or inventory skill. Do not clean data, run regressions, generate result tables, choose rules for significance, or write manuscript claims.

### Mode 2: EXECUTION_AUTOPILOT
Use only after the researcher has explicitly approved a plan and execution scope.

Automatically complete, within approved scope:

1. Execution scope lock.
2. Coding/index plan.
3. Raw data execution with read-only raw inputs and controlled derived outputs.
4. Descriptive tables.
5. Exploratory association.
6. Pilot exploratory regression if approved.
7. Figures.
8. Post-execution audit.
9. Keep/drop triage.
10. V2 revision if needed.
11. Partial commit of safe outputs, only if autopilot commit is explicitly allowed and commit safety checks pass.
12. Cleanup of untracked DROP files, only if autopilot cleanup is explicitly allowed.
13. Final handoff package.
14. Handoff commit, only if autopilot commit is explicitly allowed and commit safety checks pass.

Then stop and report final status.

## orchestrated_skills

- `project-intake`
- `identification-proposal`
- `data-inventory-audit`
- `data-cleaning`
- `variable-construction`
- `descriptive-statistics`
- `pre-regression-proposal`
- `regression-spec-audit`
- `baseline-regression`
- `event-study`
- `robustness-checks`
- `heterogeneity-mechanism`
- `table-output-audit`
- `handoff-package-builder`

Call only the skills needed for the selected mode and approved scope. If a specialized skill has stricter rules, follow the stricter rule.

## required_inputs

For `PLAN_AUTOPILOT`:

- `project_name`
- `project_title`
- `research_question`
- `raw_data_path`
- `main_language`
- `secondary_language`
- `unit_of_observation`
- `preferred_analysis_scope`
- `forbidden_claims`
- `whether_exploratory_regression_allowed`
- `whether_autopilot_commit_allowed`
- `whether_autopilot_cleanup_allowed`

### minimal-start prompt defaults

If the researcher asks to `初始化并启动` a new project and provides only these minimum fields, treat it as a valid Productized Regression Pipeline start request:

- `project_name` from `项目名`
- `project_title` from `论文题目`
- `raw_data_path` from `主数据`
- `main_language` from `主语言`
- `secondary_language` from `次语言`
- `research_question` from `研究问题`

Apply these safe defaults for missing PLAN fields:

- `unit_of_observation`: `needs_author_input`
- `preferred_analysis_scope`: `identification_and_data_processing_proposal_only`
- `forbidden_claims`: `no manuscript prose, no causal conclusion, no mechanism claim`
- `whether_exploratory_regression_allowed`: `PLAN_ONLY`
- `whether_autopilot_commit_allowed`: `YES for scaffold only`
- `whether_autopilot_cleanup_allowed`: `NO`

For this short start request, bootstrap the project, create the safe scaffold commit, read generated rules and method cards, enter `PLAN_AUTOPILOT`, and stop at the `Identification Strategy Gate`. Do not clean data, construct variables, run descriptive statistics, execute regressions, or write manuscript prose.

When stopping at the `Identification Strategy Gate` after a short start request, the user-facing response must not only say that execution stopped or write `needs_author_input` into files. It must use the fixed `## Stop Message` template and include:

- `why stopped`: 用中文说明识别策略、样本规则、变量定义、处理分配方式和设计类型仍需要研究者确认。
- `current status`: 用中文列出本轮已经完成的 scaffold、intake、规则、proposal、gate-status、risk 或 commit artifacts。
- `current problems`: 用中文列出 P0 blockers、P1 risks、P2 issues 和 approval-gate boundaries；空项写 `none`。
- `questions for researcher`: 用中文提出最少作者输入问题，并按 `must answer before identification proposal`、`can be supplied later`、`answer only if external/linkable data exist` 分组。
- `blocked boundary`: 用中文说明不得继续 data cleaning、variable construction、descriptive statistics、regression execution、manuscript prose、causal conclusion 或 mechanism claim。
- `required user action`: 用中文列出需要研究者回答、确认、修正文件或批准的事项。
- `next action after response`: 用中文说明下一步是 written identification-strategy proposal，并在任何 execution approval 前分类 feasible 和 infeasible designs。
- `project record paths`: 列出 generated or updated planning、gate-status、risk、proposal 和 commit-log files；路径保持原文。

The minimum questions must cover observation unit, time structure, treatment/exposure measurement, outcome measurement, mechanism or mediator data, merge/linkage fields, data license and confidentiality boundaries, and intended evidence positioning. Asking these questions is part of the gate interaction; it does not authorize data cleaning, variable construction, descriptive statistics, regression execution, or manuscript claims.

For `EXECUTION_AUTOPILOT`:

- Explicit researcher approval selecting a plan.
- Approved execution scope.
- Approved identification strategy, sample rules, merge keys, variable construction rules, fixed effects, clustering, controls, estimator, output scope, robustness matrix, and exploratory-regression permission where relevant.
- Existing planning artifacts and gate records from `PLAN_AUTOPILOT` or equivalent human-approved materials.

## required_outputs

The orchestrator must maintain these run-level records:

- `review/pipeline_run_summary.md`
- `review/pipeline_gate_status.md`
- `review/pipeline_commit_log.md`
- `review/pipeline_remaining_risks.md`
- `review/pipeline_next_actions.md`

Mode-specific skills may add their own required outputs. All outputs must be traceable to scripts, logs, proposals, researcher decisions, or audit records.

## human_gates

Stop and wait for the researcher only in these cases:

1. A recommended plan or alternative plan needs researcher approval.
2. The researcher chooses `REVISE_AND_RESUBMIT`.
3. Raw data safety preflight fails.
4. PII or open-text leakage risk cannot be automatically excluded.
5. Proposed execution exceeds approved scope.
6. A formal causal identification claim appears.
7. The user explicitly requests manual review.
8. The final handoff package is completed.
9. A data-processing or specification recommendation would depend on favorable statistical significance.

Every stop-and-wait case must produce a user-facing `Stop Message`; do not only write `review/pipeline_gate_status.md`, `review/pipeline_remaining_risks.md`, or `review/pipeline_next_actions.md`. The message must contain `why stopped`, `current status`, `current problems`, `questions for researcher`, `blocked boundary`, `required user action`, `next action after response`, and `project record paths`.

In every Stop Message, keep fixed field names in English but write field values in Chinese whenever practical. Keep variables, formulas, code, paths, commands, schema fields, Stata package names, model names, and other technical identifiers in their original form. This Chinese-language rule does not apply to formal tables, figures, table notes, figure notes, captions, labels, legends, or LaTeX/RTF/XLSX output.

Use this fixed template for every stop-and-wait case:

```markdown
## Stop Message

- why stopped: <用中文说明 exact gate, blocker, manual-review request, handoff boundary, or approved-scope boundary>
- current status: <用中文说明本轮已完成事项和已生成或更新的 artifacts>
- current problems:
  - P0: <用中文说明 blocking issues, or none>
  - P1: <用中文说明 material disclosed risks, or none>
  - P2: <用中文说明 format/minor issues, or none>
- questions for researcher:
  1. <用中文提出需要回答或确认的具体问题>
  2. <用中文提出需要回答或确认的具体问题>
- blocked boundary: <用中文说明用户回复前 agent 不得继续做什么>
- required user action: <用中文说明需要的确认、修正、artifact、path、approval 或 decision>
- next action after response: <用中文说明用户回复后 agent 将执行什么>
- project record paths: <relevant proposal/gate/risk/failure/audit/handoff files>
```

If no problems or no researcher questions exist, write `current problems: none` or `questions for researcher: none` explicitly. P1 and P2 issues do not trigger a stop by themselves, but when the orchestrator stops for any other reason, include current P1/P2 risks in `current problems`. Approval-gate stops must include answerable questions or confirmation items; do not write only "please confirm."

Minimum stop prompts by case:

1. Recommended plan approval: in `questions for researcher`, list the plan options, the recommended option, and the exact approval wording or revision request needed; in `blocked boundary`, state what execution remains blocked.
2. `REVISE_AND_RESUBMIT`: in `current problems`, list the revision issues and files to revise; in `next action after response`, state whether the next step is a revised proposal or a narrower execution scope.
3. Raw data safety preflight failure: in `current problems`, list the unsafe path or Git exposure; in `blocked boundary`, prohibit data execution; in `questions for researcher`, ask for a safe data location or permission to repair tracking rules.
4. PII or open-text leakage risk: in `current problems`, list the risky fields or files; in `blocked boundary`, prohibit export or analysis of sensitive content; in `questions for researcher`, ask for anonymization, exclusion, or approved handling.
5. Execution beyond approved scope: in `current problems`, name the attempted extra scope; in `blocked boundary`, prohibit that execution; in `questions for researcher`, ask for explicit scope expansion or a narrowed run.
6. Formal causal identification claim: in `current problems`, quote or summarize the unsafe claim; in `blocked boundary`, prohibit causal language and causal execution; in `questions for researcher`, ask for approved identification evidence or wording downgrade.
7. Manual review request: in `current status`, state what is ready for review; in `blocked boundary`, state what remains blocked during review; in `questions for researcher`, state what decision is needed to resume.
8. Final handoff completed: in `current status`, state completion status and handoff package path; in `current problems`, state P0/P1/P2 status; in `questions for researcher`, ask whether transfer to `empirical-paper-agent` is approved.
9. Significance-dependent recommendation risk: in `current problems`, identify the recommendation that appears result-driven; in `blocked boundary`, prohibit significance-driven selection; in `questions for researcher`, ask for a design-based rule or rejection.

Do not stop for P1 risks, low N, sparse variables, failed models, table formatting revisions, figure redo needs, or appendix downgrade decisions. Record, skip, revise, downgrade, or route to appendix as appropriate.

## P0_P1_handling

### P0

- Stop immediately.
- Do not continue execution.
- Output a P0 report in `review/pipeline_gate_status.md` and `review/pipeline_remaining_risks.md`.
- Include the user-facing `Stop Message` with the P0 reason, current status, current problems, researcher questions, blocked boundary, required user action, next action after response, and project record paths.
- Do not commit unsafe results.
- Do not treat partial results as successful evidence.

Examples include raw data modification, unsafe raw-data Git exposure, unapproved execution, unapproved sample deletion, PII/open-text leakage that cannot be excluded, execution beyond approved scope, regression without required logs, failed regression reported as success, and formal causal identification language without documented approval and evidence.

### P1

- Do not stop.
- Record the issue in `review/pipeline_remaining_risks.md` and the relevant skill-level risk register.
- Continue execution within approved scope.
- Downgrade claim language to cautious wording such as `descriptive pattern`, `association`, `exploratory`, or `suggestive pilot evidence`.
- Keep P1 risks visible in final handoff.

Examples include low N, sparse variables, subjective self-reports, common method bias, incomplete labels, weak proxy coverage, unstable formatting, and models that should be skipped or moved to appendix.

## autopilot_commit_rules

Autopilot commits are allowed only when the researcher has explicitly set `whether_autopilot_commit_allowed: YES`.

Before each commit:

1. Run `git status --short`.
2. Verify raw data are not tracked.
3. Verify raw-data paths are covered by `.gitignore`.
4. Verify all staged files are on the safe whitelist.
5. Do not commit raw data, Excel files, logs, PII, open-text original responses, individual-level data, compressed archives, or binary statistical data.
6. Use a clear commit message such as `Add autopilot proposal package` or `Add audited handoff package`.
7. After committing, record the commit hash in `review/pipeline_commit_log.md`.

Safe whitelist:

- Framework instructions.
- Project-level rules and method cards.
- Project metadata with no PII.
- Proposals.
- Decision sheets.
- Audit summaries.
- Risk registers.
- File inventories that do not reveal sensitive individual-level content.
- Table/figure inventories.
- Handoff README and manifests that exclude sensitive content.

Unsafe by default:

- `projects/*/data/raw*/`
- `projects/*/output/logs/`
- `projects/*/handoff_package/logs/`
- `*.xlsx`
- `*.xls`
- `*.dta`
- `*.sav`
- `*.parquet`
- `*.zip`
- `*.rar`
- `*.7z`
- Any file containing PII, open-text original responses, or individual-level rows.

## revision_rules

If post-execution audit marks a table or figure as `REVISE`:

1. Do not stop to ask the researcher.
2. Generate a v2 artifact.
3. Do not overwrite the old artifact.
4. Audit v2.
5. Submit or commit only v2 if commit is allowed and safety checks pass.
6. Record the revision in the revision report and `review/pipeline_run_summary.md`.

If post-execution audit marks a table or figure as `DROP`:

1. Do not commit it.
2. If it is untracked and autopilot cleanup is explicitly allowed, clean it after audit.
3. Do not delete tracked files unless the researcher explicitly allows deletion.
4. Record the drop reason in `review/pipeline_remaining_risks.md` or the relevant audit report.

## pilot_regression_rules

If the approved researcher decision allows exploratory regression, automatically enter the pilot exploratory regression package. Do not stop to ask whether regression should begin.

Rules:

- Use only approved chain nodes.
- A/B/G nodes must not enter regression unless explicitly approved.
- Do not run complete mediation.
- Do not run a formal causal model.
- Mark all such outputs as `pilot exploratory regression`.
- Record failed or skipped models in `failed_regressions.md`.
- Never treat a failed regression as successful evidence.

## claim_boundary

Do not write or imply these phrases as positive empirical claims at any stage:

- `causal effect`
- `exogenous shock`
- `complete mediation`
- `formal identification`
- `objective street upgrade`
- `房价下行导致`
- `因果效应`
- `外生冲击`
- `正式识别`

These terms may appear only in a handoff or claim-boundary file that labels them as forbidden language, future data needs, or unresolved P0 boundaries.

## PLAN_AUTOPILOT_workflow

1. Create or update pipeline status files.
2. Scaffold the project with `project_initializer.py` only if a project workspace is authorized.
3. Run raw-data safety preflight through inventory/audit mechanisms without modifying data.
4. Run limited intake and metadata gap marking.
5. Draft a variable dictionary from documented metadata and allowed previews only.
6. Invoke `identification-proposal` to produce the identification-tree path, candidate Y/X/unit/time/proxy variables, feasible designs, infeasible designs, method-card references, diagnostics, and risk register.
7. Invoke `data-cleaning` in proposal mode to prepare the data-processing gate covering unit, time, keys, deduplication, sample, missing, outliers, variable formulas, event windows, multiple treatment, and control-group rules.
8. Invoke `pre-regression-proposal` to create the recommendation, alternatives, decision sheet, and risk register.
9. If autopilot commit is allowed, commit only safe proposal artifacts after commit safety checks.
10. Stop for researcher approval.

## EXECUTION_AUTOPILOT_workflow

1. Verify explicit researcher approval and lock execution scope.
2. Refuse execution if approval is absent, ambiguous, silent, broader than documented, or missing the identification and data-processing gates.
3. Generate coding/index plan within approved scope.
4. Execute approved raw-data workflows with read-only raw data and controlled derived outputs.
5. Generate descriptive tables and figures.
6. Run exploratory association and pilot exploratory regression only if approved.
7. Audit all outputs for traceability, logs, sample, FE, clustering, controls, notes, claim labels, and no significance-driven selection.
8. Automatically revise `REVISE` outputs as v2, skip or drop unsafe outputs, and record failures.
9. If autopilot commit is allowed, commit safe audited outputs after safety checks.
10. If autopilot cleanup is allowed, clean only untracked DROP files.
11. Build the final handoff package.
12. If autopilot commit is allowed, commit the safe handoff package after safety checks.
13. Stop and report final status.

## completion_criteria

The orchestrator run is complete only when:

- It reaches the next required gate or final handoff.
- Required pipeline status outputs exist.
- P0 blockers are either absent or clearly reported.
- P1 risks are recorded and do not interrupt the run.
- Researcher approval gates remain explicit and uncleared by silence.
- Any commits were performed only after safety checks and have recorded hashes.
- No raw data were modified.
- No unsupported causal or manuscript claim was written.
