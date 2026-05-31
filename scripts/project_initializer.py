"""Initialize an empirical-regression-agent project scaffold.

The initializer is dry-run by default. With ``--execute`` it creates a
project workspace, project-level rules, method cards, and generic config/code
templates. It never creates empirical results or manuscript prose.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path


PROJECT_DIRS = [
    "data",
    "data/raw",
    "data/processed",
    "data/external",
    "code",
    "config",
    "output",
    "output/plans",
    "output/tables",
    "output/figures",
    "output/logs",
    "references",
    "references/method-cards",
    "rules",
    "review",
    "review/hitl",
    "handoff_package",
]

GITKEEP_DIRS = [
    "data/raw",
    "data/processed",
    "data/external",
    "output/tables",
    "output/figures",
    "output/logs",
]

RULE_FILES = {
    "PROJECT_RULES.md": """# PROJECT_RULES.md - {project_title} project rules

## Project Information

- Project name: {project_name}
- Project title: {project_title}
- Owner: {owner}
- Created by: empirical-regression-agent project initializer
- Main data: {main_data}
- Main language: {main_language}
- Secondary language: {secondary_language}
- Research question: {research_question}
- Compliance baseline: {compliance_baseline}

## Operating Boundary

This project is governed by `empirical-regression-agent`. The agent may create
reproducible empirical artifacts, execution logs, tables, figures, audits, and
handoff packages. It must not write manuscript body text, invent empirical
content, or convert unaudited outputs into causal claims.

Empty data and output directories may contain `.gitkeep` files so the scaffold
can be reproduced after cloning. These placeholders do not authorize committing
raw data, derived data, logs, or empirical outputs.

## Required Rule Files

- `rules/reproducibility-rules.md`
- `rules/data-processing-rules.md`
- `rules/disclosure-and-license-rules.md`

## Approval Gates

Researcher approval is required before sample-screening rules, merge keys,
variable formulas, outlier handling, main specifications, fixed effects,
clustering, controls, event-study windows, robustness matrices, heterogeneity
or mechanism-related designs, final table order, or paper-agent handoff.

## No Significance-Driven Changes

The agent may report sensitivity patterns, including sign, magnitude, standard
errors, and significance changes across pre-declared specifications. It must
not choose cleaning rules, samples, variables, fixed effects, clustering,
estimators, or table inclusion because they produce more significant results.
""",
    "rules/reproducibility-rules.md": """# Reproducibility Rules

## Path Rules

- `data/raw/`: raw data. Read-only. No script may write here.
- `data/processed/`: derived analysis data written only by approved cleaning or
  construction scripts.
- `data/external/`: documented external reference data.
- `code/`: all Stata, Python, or helper scripts.
- `output/tables/`: generated tables.
- `output/figures/`: generated figures.
- `output/logs/`: complete execution logs.
- `.gitkeep` files may be committed only to preserve empty directories. They do
  not make data, logs, tables, or figures safe to commit.

## Random Seeds

- Project seed: `{project_seed}`.
- Stata workflows must call `set seed {project_seed}` before bootstrap,
  random sampling, simulation, or randomized procedures.
- Independent seeds should use the project seed plus a documented integer
  offset.

## Software Version Lock

- Stata do-files must begin with `version {stata_version}`.
- Python workflows must record the interpreter version and package versions in
  the project README or environment file.
- Package upgrades must be documented and synchronized before rerunning final
  outputs.
""",
    "rules/data-processing-rules.md": """# Data Processing Rules

## Variable Naming

- Use lowercase snake_case variable names.
- Time variables should use stable names such as `year`, `ym`, `yq`, or
  documented event-time variables.
- Treatment indicators should use `treat_*`; outcomes should use `y_*` or
  semantic names documented in the variable dictionary.
- Fixed effects must be absorbed by estimators such as `absorb()`, not expanded
  into large manual dummy sets in the analysis data.

## Data-Processing Approval Gate

The agent must propose and the researcher must approve these items before
execution: unit of observation, time definition, primary keys, merge keys,
deduplication rules, sample boundaries, missing-value handling, unreasonable
value handling, outlier handling, variable units, frequency alignment, panel
balance, event windows, multiple treatment handling, control-group definition,
variable construction formulas, leads/lags, and geographic, industry, or
administrative matching rules.

## Evidence Standard

Every sample-changing step must have before/after counts in logs and a row in
the sample-flow record. Deduplication must retain an audit copy or versioned
record sufficient to inspect discarded alternatives.
""",
    "rules/disclosure-and-license-rules.md": """# Disclosure And License Rules

## AI Use Disclosure

This project may use AI assistance for scaffold generation, data-audit plans,
code templates, table and figure formatting, log review, and reproducibility
checks. All empirical specifications, sample rules, identification choices,
and final claims require researcher review. The final paper or appendix must
disclose AI use according to the applicable journal and AEA policy.

## Data License Statement

- Main data: `{main_data}`.
- License status: `needs_author_input`.
- Redistribution status: `needs_author_input`.
- Restricted, proprietary, individual-level, or confidential data must not be
  committed to Git or included in public reproduction packages unless the
  license explicitly permits it.

## Restricted Data Rule

If the project later uses WRDS, Compustat, CRSP, Wind, CSMAR, administrative
microdata, survey identifiers, open-text responses, or other restricted data,
the researcher must update this file and the handoff protocol before any
release package is assembled.
""",
}

METHOD_CARDS = {
    "did-checklist.md": """# DID Checklist

Use traditional DID only when treatment timing is common or the TWFE contrast is
substantively defensible. Check pre-trends with an event-study graph, document
the control group, and cluster at the treatment-assignment level. Common Stata
commands: `reghdfe`, `eventdd`, `coefplot`. Do not interpret parallel trends as
proven; report diagnostics and remaining risks.
""",
    "modern-did-checklist.md": """# Modern DID Checklist

Use modern DID for staggered adoption or heterogeneous treatment effects. State
whether controls are never-treated or not-yet-treated, define event time, and
inspect cohort support. Common commands: `csdid`, `eventstudyinteract`,
`did2s`, or stacked DID with `reghdfe`. Record omitted periods, binning, sparse
cells, and failed cohorts.
""",
    "iv-validity.md": """# IV Validity

IV requires relevance and exclusion. Report first-stage strength, the policy or
institutional source of variation, and why the instrument affects the outcome
only through the endogenous variable. Common commands: `ivreghdfe`,
`ivregress 2sls`, first-stage diagnostics, and weak-IV checks. Treat exclusion
as an assumption requiring researcher approval, not agent verification.
""",
    "rdd-bandwidth.md": """# RDD Bandwidth

RDD requires a credible cutoff, no precise manipulation around the threshold,
and smooth potential outcomes. Inspect density and covariate balance near the
cutoff. Common commands: `rdrobust`, `rddensity`, `rdplot`. Report bandwidth
choice, kernel, polynomial order, donut rules, and sensitivity to narrower and
wider windows.
""",
    "synthetic-control.md": """# Synthetic Control

Use synthetic control or SDID when one or a few units are treated and a donor
pool can approximate pre-treatment outcomes. Check donor eligibility,
pre-treatment fit, placebo gaps, and weight concentration. Common commands:
`synth`, `sdid`. Do not convert visual fit into causal certainty; disclose weak
pre-fit or limited donor support.
""",
    "matching-dml.md": """# Matching, Weighting, And DML

Use matching, IPW, AIPW, or DML when selection on observables is the maintained
assumption. Define the pre-treatment covariates before outcome inspection,
check overlap and balance, and report trimming rules. Common commands include
`teffects`, `psmatch2`, `lassopack`, and Python DML tools. Hidden post-outcome
covariate selection is not allowed.
""",
    "shift-share.md": """# Shift-Share And Exposure Designs

Exposure designs require a documented shock, predetermined exposure shares, and
a defensible exclusion argument. Check whether shares predate outcomes, whether
the shock is plausibly external, and whether standard errors account for shock
or exposure structure. Common tools include `reghdfe`, leave-one-out exposure
construction, and shock-level robustness checks.
""",
}

PLACEHOLDER_MARKERS = {
    "NEED_AUTHOR_CONFIRMATION",
    "PLACEHOLDER",
    "TBD",
    "TODO",
    "DRAFT",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Dry-run first initializer for projects/<project_name>/ using generic templates."
    )
    parser.add_argument("--project-name", required=True, help="New project directory name.")
    parser.add_argument("--project-title", default="<project_title>", help="Research project title.")
    parser.add_argument("--main-data", default="<main_data>", help="Main data file or data source.")
    parser.add_argument("--main-language", default="Stata 18", help="Main analysis language.")
    parser.add_argument("--secondary-language", default="Python", help="Secondary language.")
    parser.add_argument("--research-question", default="<research_question>", help="Research question.")
    parser.add_argument("--owner", default="[researcher name]", help="Responsible researcher or team.")
    parser.add_argument(
        "--compliance-baseline",
        default="AEA Data and Code Availability Policy v1.0",
        help="Compliance baseline for the project scaffold.",
    )
    parser.add_argument(
        "--project-root",
        required=True,
        type=Path,
        help="Parent projects directory or explicit project root parent.",
    )
    parser.add_argument(
        "--template-dir",
        required=True,
        type=Path,
        help="Directory containing generic template files.",
    )
    parser.add_argument("--execute", action="store_true", help="Actually create directories and files.")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite only existing placeholder files; never overwrite user files.",
    )
    parser.add_argument(
        "--create-initial-commit",
        action="store_true",
        help="After --execute, create a safe initial git commit for generated scaffold files.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=True,
        help="Preview actions. This is the default unless --execute is passed.",
    )
    return parser.parse_args()


def validate_project_name(name: str) -> None:
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", name):
        raise ValueError("project name may contain only letters, numbers, underscore, hyphen, and dot")
    if name in {".", ".."}:
        raise ValueError("project name must not be '.' or '..'")


def destination_for_template(template: Path) -> Path:
    name = template.name
    if name.endswith(".template.yml"):
        return Path("config") / name.replace(".template", "")
    if name.endswith(".template.csv"):
        return Path("config") / name.replace(".template", "")
    if name.endswith(".template.do"):
        return Path("code") / name.replace(".template", "")
    if name == "handoff_README.template.md":
        return Path("handoff_package") / "handoff_README.md"
    if name.endswith(".template.md"):
        return Path("review") / name.replace(".template", "")
    return Path("templates") / name


def context_from_args(args: argparse.Namespace) -> dict[str, str]:
    stata_version = "18.0"
    match = re.search(r"(\d+(?:\.\d+)?)", args.main_language)
    if match:
        stata_version = match.group(1)
        if "." not in stata_version:
            stata_version = f"{stata_version}.0"
    main_data_path = Path(args.main_data)
    source_name = main_data_path.name if main_data_path.name else args.main_data
    source_format = main_data_path.suffix.lower().lstrip(".") or "needs_author_input"
    raw_data_path = f"data/raw/{source_name}" if source_name else "data/raw/needs_author_input"
    return {
        "project_name": args.project_name,
        "project_id": args.project_name,
        "project_title": args.project_title,
        "paper_title": args.project_title,
        "main_data": args.main_data,
        "source_name": source_name,
        "source_path": raw_data_path,
        "source_format": source_format,
        "raw_data_path_read_only": raw_data_path,
        "processed_data_path": "data/processed/needs_author_input",
        "main_language": args.main_language,
        "secondary_language": args.secondary_language,
        "research_question": args.research_question,
        "owner": args.owner,
        "compliance_baseline": args.compliance_baseline,
        "project_seed": "20260417",
        "stata_version": stata_version,
        "approved_other_tool": args.secondary_language,
    }


def render_template_text(text: str, context: dict[str, str]) -> str:
    replacements = {
        "<project_name>": context["project_name"],
        "<project_id>": context["project_id"],
        "<project_title>": context["project_title"],
        "<paper_title>": context["paper_title"],
        "<owner>": context["owner"],
        "<source_name>": context["source_name"],
        "<source_path>": context["source_path"],
        "<source_format>": context["source_format"],
        "<raw_data_path_read_only>": context["raw_data_path_read_only"],
        "<processed_data_path>": context["processed_data_path"],
        "<stata_version>": context["stata_version"],
        "<approved_other_tool>": context["approved_other_tool"],
    }
    for placeholder, value in replacements.items():
        text = text.replace(placeholder, value)
    text = text.replace(
        'project_stage: "<intake|data_audit|cleaning_proposal|variable_construction|regression_execution|audit|handoff|replay_validation>"',
        "project_stage: intake",
    )
    text = text.replace('read_only_required: "<true|false>"', "read_only_required: true")
    text = text.replace(
        'status: "<available|missing|needs_author_input|unavailable_by_design>"',
        "status: needs_author_input",
    )
    return text


def is_placeholder_file(path: Path) -> bool:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return False
    upper = text.upper()
    return any(marker in upper for marker in PLACEHOLDER_MARKERS)


def copy_template(src: Path, dst: Path, execute: bool, force: bool) -> str:
    if dst.exists():
        if not force:
            return f"SKIP existing user file: {dst}"
        if not is_placeholder_file(dst):
            return f"SKIP non-placeholder existing file: {dst}"
        action = "OVERWRITE placeholder"
    else:
        action = "CREATE"

    if execute:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    return f"{action}: {src} -> {dst}"


def copy_template_rendered(src: Path, dst: Path, execute: bool, force: bool, context: dict[str, str]) -> str:
    if dst.exists():
        if not force:
            return f"SKIP existing user file: {dst}"
        if not is_placeholder_file(dst):
            return f"SKIP non-placeholder existing file: {dst}"
        action = "OVERWRITE placeholder"
    else:
        action = "CREATE"

    if execute:
        dst.parent.mkdir(parents=True, exist_ok=True)
        text = src.read_text(encoding="utf-8")
        with dst.open("w", encoding="utf-8", newline="\n") as handle:
            handle.write(render_template_text(text, context))
    return f"{action}: {src} -> {dst}"


def write_text_file(path: Path, text: str, execute: bool, force: bool) -> str:
    if path.exists():
        if not force:
            return f"SKIP existing user file: {path}"
        if not is_placeholder_file(path):
            return f"SKIP non-placeholder existing file: {path}"
        action = "OVERWRITE placeholder"
    else:
        action = "CREATE"

    if execute:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
    return f"{action}: {path}"


def generated_files(project_root: Path) -> list[Path]:
    allowed_roots = {"code", "config", "review", "rules", "references", "handoff_package"}
    allowed_top_level = {"PROJECT_RULES.md"}
    unsafe_dirs = {
        ("data", "raw"),
        ("data", "processed"),
        ("output", "logs"),
        ("handoff_package", "logs"),
    }
    unsafe_suffixes = {".xlsx", ".xls", ".dta", ".sav", ".parquet", ".zip", ".rar", ".7z"}

    files: list[Path] = []
    for path in sorted(project_root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(project_root)
        parts = rel.parts
        if any(part == ".git" for part in parts):
            continue
        if path.name == ".gitkeep":
            files.append(path)
            continue
        if len(parts) >= 2 and (parts[0], parts[1]) in unsafe_dirs:
            continue
        if path.suffix.lower() in unsafe_suffixes:
            continue
        if len(parts) == 1 and parts[0] in allowed_top_level:
            files.append(path)
            continue
        if parts and parts[0] in allowed_roots:
            files.append(path)
    return files


def create_initial_commit(project_root: Path) -> int:
    unsafe_parts = {
        ("data", "raw"),
        ("data", "processed"),
        ("output", "logs"),
        ("handoff_package", "logs"),
    }
    files = [path for path in generated_files(project_root) if path.exists()]
    for path in files:
        rel = path.relative_to(project_root)
        parts = rel.parts
        if path.name == ".gitkeep":
            continue
        if len(parts) >= 2 and (parts[0], parts[1]) in unsafe_parts:
            print(f"P0: unsafe path selected for commit: {path}", file=sys.stderr)
            return 2

    if not files:
        print("P0: no generated files exist for initial commit", file=sys.stderr)
        return 2

    if not (project_root / ".git").exists():
        print("INITIAL COMMIT: creating project-local git repository.")
        try:
            subprocess.run(["git", "-C", str(project_root), "init"], check=True)
        except subprocess.CalledProcessError as exc:
            print(f"P0: git init failed: {exc}", file=sys.stderr)
            return 2
    else:
        print("INITIAL COMMIT: using existing project-local git repository.")

    try:
        subprocess.run(["git", "-C", str(project_root), "rev-parse", "--show-toplevel"], check=True, capture_output=True, text=True)
        rel_files = [str(path.relative_to(project_root)) for path in files]
        print("INITIAL COMMIT: staging safe scaffold files:")
        for rel_file in rel_files:
            print(f"  - {rel_file}")
        subprocess.run(["git", "-C", str(project_root), "add", *rel_files], check=True)
        subprocess.run(
            [
                "git",
                "-C",
                str(project_root),
                "-c",
                "user.name=empirical-regression-agent",
                "-c",
                "user.email=empirical-regression-agent@example.invalid",
                "commit",
                "-m",
                "[init] scaffold empirical regression project",
            ],
            check=True,
        )
        print("INITIAL COMMIT: created [init] scaffold empirical regression project.")
    except subprocess.CalledProcessError as exc:
        print(f"P0: initial commit failed: {exc}", file=sys.stderr)
        return 2
    return 0


def main() -> int:
    args = parse_args()
    try:
        validate_project_name(args.project_name)
    except ValueError as exc:
        print(f"P0: invalid project name: {exc}", file=sys.stderr)
        return 2

    project_root = (args.project_root / args.project_name).resolve()
    template_dir = args.template_dir.resolve()
    execute = bool(args.execute)
    context = context_from_args(args)

    if not template_dir.exists():
        print(f"P0: template directory does not exist: {template_dir}", file=sys.stderr)
        return 2

    print("DRY RUN: no files will be created." if not execute else "EXECUTE: creating generic project scaffold.")
    print(f"Project root: {project_root}")

    for rel_dir in PROJECT_DIRS:
        target = project_root / rel_dir
        print(f"{'CREATE' if execute else 'WOULD CREATE'} dir: {target}")
        if execute:
            target.mkdir(parents=True, exist_ok=True)

    for rel_dir in GITKEEP_DIRS:
        dst = project_root / rel_dir / ".gitkeep"
        print(write_text_file(dst, "", execute=execute, force=args.force))

    for rel_path, template_text in RULE_FILES.items():
        dst = project_root / rel_path
        print(write_text_file(dst, template_text.format(**context), execute=execute, force=args.force))

    for name, text in METHOD_CARDS.items():
        dst = project_root / "references" / "method-cards" / name
        print(write_text_file(dst, text, execute=execute, force=args.force))

    templates = sorted(p for p in template_dir.iterdir() if p.is_file() and ".template." in p.name)
    for src in templates:
        dst = project_root / destination_for_template(src)
        if src.name == "project_metadata.template.yml":
            print(copy_template_rendered(src, dst, execute=execute, force=args.force, context=context))
        else:
            print(copy_template(src, dst, execute=execute, force=args.force))

    if args.create_initial_commit:
        if not execute:
            print("P0: --create-initial-commit requires --execute", file=sys.stderr)
            return 2
        commit_rc = create_initial_commit(project_root)
        if commit_rc != 0:
            return commit_rc

    print("No concrete variables, regression results, or manuscript text were generated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
