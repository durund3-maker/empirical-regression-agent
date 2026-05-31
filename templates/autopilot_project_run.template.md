# Autopilot Project Run Template

Fill this file before asking `pipeline-orchestrator` to start a project run.

## Required Fields

- `project_name`:
- `research_question`:
- `raw_data_path`:
- `unit_of_observation`:
- `preferred_analysis_scope`:
- `forbidden_claims`:
- `whether_exploratory_regression_allowed`: YES / NO / PLAN_ONLY
- `whether_autopilot_commit_allowed`: YES / NO
- `whether_autopilot_cleanup_allowed`: YES / NO

## Notes

- `PLAN_ONLY` for exploratory regression means the agent may propose it but must not execute it before approval.
- `whether_autopilot_commit_allowed: YES` permits commits only after the pipeline commit safety checks pass.
- `whether_autopilot_cleanup_allowed: YES` permits cleanup only for untracked DROP files after audit.
- Researcher silence is not approval.
- A recommended plan is not approval.
- Formal causal identification P0 cannot be cleared by this template or by `pipeline-orchestrator`.
- A short `initialize and start` request defaults to bootstrap plus `PLAN_AUTOPILOT`, stopping at the `Identification Strategy Gate`.

## Minimal Start Prompt

```text
Please use empirical-regression-agent to initialize and start a new research project.

Project initialization fields:
- project_name: <project_name>
- paper_title: <paper_title>
- main_data: <main_data_file_or_path>
- main_language: Stata 18
- secondary_language: Python
- research_question: <how X affects Y>
```

Default interpretation: initialize the project, generate rules and method cards, create the safe project-local scaffold commit, read generated rules, enter `PLAN_AUTOPILOT`, and stop at the `Identification Strategy Gate`. Do not clean data, construct variables, run descriptive statistics, run regressions, write manuscript prose, or write causal/mechanism claims.

## Identification Gate Stop Message Template

Use the fixed `## Stop Message` template in the user-facing final reply and in the project planning record when a short start request stops at the `Identification Strategy Gate`.

Keep fixed field names in English, but write field values in Chinese whenever practical. Keep variables, formulas, code, paths, commands, schema fields, Stata package names, model names, and other technical identifiers in their original form.

```markdown
## Stop Message

- why stopped: 停止在 `Identification Strategy Gate`，因为 identification strategy、sample rules、variable definitions、treatment assignment 和 design family 需要研究者确认。
- current status: <用中文列出本轮已完成的 project scaffold、safe commit if created、rules、method cards、planning records、proposal records、gate-status files 或 risk files>
- current problems:
  - P0: <用中文说明 blocking identification, data-safety, approval, or scope issues, or none>
  - P1: <用中文说明 material disclosed risks, or none>
  - P2: <用中文说明 format/minor issues, or none>
- questions for researcher:
  - must answer before identification proposal:
    1. observation unit：请确认一行观测是 store、founder、street block、city-year，还是其他已记录单位。
    2. time structure：请确认数据是否包含 opening time、survey time、housing-price decline timing 或 panel structure。
    3. treatment/exposure measurement：请说明 treatment/exposure 如何度量。
    4. outcome measurement：请说明 outcome 如何度量。
    5. intended evidence positioning：请确认目标是 strict causal identification、mechanism exploration、descriptive facts、association analysis，还是 mixed-method evidence。
  - can be supplied later:
    1. mechanism or mediator data：请说明机制或中介变量是否有 documented source fields 或 external support。
    2. data license and confidentiality boundaries：请说明数据是否 restricted、confidential、redistributable，或是否可安全进行 read-only structure inspection。
  - answer only if external/linkable data exist:
    1. merge/linkage fields：如存在外部或可链接数据，请说明 address、city、district、street、year、entity name、business registration ID 或其他 keys 能否连接 main data 与 external data。
- blocked boundary: 在 required gate 获得批准前，不得 clean data、construct variables、run descriptive statistics、execute regressions、export empirical tables or figures、write manuscript prose、write causal conclusions 或 write mechanism claims。
- required user action: 请回答上述 author-input questions，或提供可解决这些问题的 corrected project metadata/source notes。
- next action after response: 用户回复后，agent 将准备 written identification-strategy proposal，并在任何 execution approval 前分类 feasible 和 infeasible design families。
- project record paths: <relevant PROJECT_RULES.md, config/project_metadata.yml, review/identification_strategy_proposal.md, review/pipeline_gate_status.md, review/pipeline_remaining_risks.md, review/pipeline_next_actions.md, or commit log paths>
```

If there are no P0, P1, or P2 problems in a specific run, write `none` for the empty severity class. Do not replace this user-facing Stop Message with only `needs_author_input` fields or project record paths.

## A. PLAN_AUTOPILOT Prompt

```text
Use the pipeline-orchestrator skill in PLAN_AUTOPILOT mode.

Project fields:
- project_name:
- research_question:
- raw_data_path:
- unit_of_observation:
- preferred_analysis_scope:
- forbidden_claims:
- whether_exploratory_regression_allowed:
- whether_autopilot_commit_allowed:
- whether_autopilot_cleanup_allowed:

Run to the next required approval gate. Automatically complete raw data safety check, project scaffold if authorized, limited intake, variable dictionary draft, causal chain mapping, pilot analysis plan, pre-execution proposal, and proposal package commit if explicitly allowed and safe. Stop only for P0 blockers or the researcher approval gate. Do not run regressions, do not generate empirical results, do not read raw data beyond allowed safety/inventory checks, and do not write manuscript claims.
```

## B. EXECUTION_AUTOPILOT Prompt

```text
Use the pipeline-orchestrator skill in EXECUTION_AUTOPILOT mode.

Approved decision:
- selected_plan:
- approved_scope:
- approved_sample_rules:
- approved_merge_keys:
- approved_variable_construction:
- approved_fixed_effects:
- approved_clustering:
- approved_controls:
- approved_estimator:
- approved_outputs:
- exploratory_regression_allowed: YES / NO
- A_B_G_regression_allowed: YES / NO
- whether_autopilot_commit_allowed:
- whether_autopilot_cleanup_allowed:

Run within the approved scope until final handoff completion. Automatically perform execution scope lock, coding/index plan, approved raw data execution, descriptive tables, exploratory association, approved pilot exploratory regression, figures, post-execution audit, keep/drop triage, v2 revision, safe partial commits if allowed, cleanup of untracked DROP files if allowed, final handoff package, and handoff commit if allowed. Stop only for P0 blockers, execution beyond approved scope, manual-review requests, or completed final handoff. Treat P1 risks as recorded cautions, not interruption points.
```
