"""Validate repository-level framework completeness without creating projects or running Stata."""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path


REQUIRED_TOP_LEVEL = ["AGENTS.md", "WORKFLOW.md", "agent_core", "config", "skills", "agents", "templates", "scripts"]
REQUIRED_SUBAGENTS = [
    "dataprep-agent.md",
    "estimator-agent.md",
    "table-agent.md",
    "reviewer-agent.md",
    "handoff-agent.md",
]
REQUIRED_TEMPLATES = [
    "project_metadata.template.yml",
    "regression_specs.template.yml",
    "robustness_matrix.template.yml",
    "variable_dictionary.template.csv",
    "table_plan.template.csv",
    "sample_flow.template.csv",
    "evidence_map.template.csv",
    "file_manifest.template.csv",
    "stata_master_do.template.do",
    "regression_run_report.template.md",
    "failed_regressions.template.md",
    "final_regression_audit.template.md",
    "handoff_README.template.md",
]
REQUIRED_SCRIPTS = [
    "project_initializer.py",
    "data_safety_check.py",
    "regression_spec_validator.py",
    "stata_log_parser.py",
    "table_inventory_builder.py",
    "evidence_map_builder.py",
    "sample_flow_checker.py",
    "stata_runner_wrapper.py",
    "handoff_manifest_builder.py",
    "replay_validation.py",
    "README.md",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check framework completeness for replay validation.")
    parser.add_argument("--repo-root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--fail-on-p0", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.repo_root.resolve()
    root_display = args.repo_root
    p0: list[str] = []
    for rel in REQUIRED_TOP_LEVEL:
        if not (root / rel).exists():
            p0.append(f"Missing top-level framework path: {rel}")
    skills_dir = root / "skills"
    if skills_dir.exists():
        for skill_dir in [p for p in skills_dir.iterdir() if p.is_dir()]:
            if not (skill_dir / "SKILL.md").exists():
                p0.append(f"Skill missing SKILL.md: {skill_dir.name}")
    else:
        p0.append("Missing skills directory")
    for rel in REQUIRED_SUBAGENTS:
        if not (root / "agents" / rel).exists():
            p0.append(f"Missing subagent: {rel}")
    for rel in REQUIRED_TEMPLATES:
        if not (root / "templates" / rel).exists():
            p0.append(f"Missing template: {rel}")
    for rel in REQUIRED_SCRIPTS:
        if not (root / "scripts" / rel).exists():
            p0.append(f"Missing script: {rel}")

    lines = [
        "# Replay Validation",
        "",
        f"- Generated: {datetime.now().isoformat(timespec='seconds')}",
        f"- Repo root: `{root_display}`",
        "- Scope: framework completeness only; no project was created and Stata was not run.",
        "",
        "## P0 Findings",
        "",
    ]
    lines += [f"- {item}" for item in p0] if p0 else ["No P0 framework completeness findings detected."]
    output = args.output if args.output.is_absolute() else root / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote replay validation report to {output}")
    return 1 if p0 and args.fail_on_p0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
