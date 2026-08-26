# Quickstart: Validate the Skill Research Design

This guide validates the local research artifact without installing or executing
any third-party skill.

## Prerequisites

- Run commands from the repository root.
- Spec Kit CLI 1.0.0 or later.
- Git.
- Python is optional and is used only for local YAML/JSON parsing.
- Do not provide credentials or project data to any candidate.

## 1. Confirm the feature location

    Get-Content .specify/feature.json
    Test-Path specs/001-research-skills/spec.md
    Test-Path specs/001-research-skills/plan.md

Expected result: feature.json points to specs/001-research-skills, and both
feature artifacts exist.

## 2. Resolve the active Spec Kit template

    specify preset resolve spec-template
    specify preset resolve plan-template

Expected result: both commands resolve a local or bundled template path without
an error. The resolved template must remain compatible with the project preset.

## 3. Check specification quality

    rg -n "\[NEEDS CLARIFICATION|ACTION REQUIRED|\[FEATURE|\[DATE|\[PROJECT_NAME" specs/001-research-skills
    git diff --check

Expected result: the first command returns no unresolved placeholder lines in
the feature artifacts, and git diff --check returns no whitespace errors.

## 4. Check the two-domain boundary

Review research.md and verify:

1. Broad scientific entries are limited to literature, writing, citations,
   notebooks, experiment design, open science, or cross-domain research.
2. Bioinformatics entries are limited to bioinformatics-specific skills or
   bounded execution capabilities.
3. No candidate is repeated across the two sections.
4. Each candidate has a source URL, invocation class, score, tier, and next
   action, or is explicitly marked evidence-incomplete.

Expected result: the catalog has at least 6 broad scientific candidates and at
least 8 bioinformatics candidates.

## 5. Validate contract files

    Get-ChildItem specs/001-research-skills/contracts/*.yml
    rg -n "name:|version:|required:|properties:|admission_rules:" specs/001-research-skills/contracts

Expected result: candidate-record.yml, invocation-contract.yml, and
scoring-record.yml exist and contain their required sections.

If a YAML parser is available, run:

    python -c "from pathlib import Path; import yaml; [yaml.safe_load(p.read_text(encoding='utf-8')) for p in Path('specs/001-research-skills/contracts').glob('*.yml')]; print('YAML contracts: OK')"

Expected result: YAML contracts: OK.

## 6. Verify the admission gate

For every candidate marked preferred-pilot:

- Confirm the score is at least 4.0.
- Confirm no critical license, sensitive-data, unsafe-default, or
  non-reproducible-entrypoint failure is present.
- Confirm an explicit QC, provenance, and human-review boundary is recorded.

Expected result: a candidate with an unresolved license or permission problem
is wrapper-needed or reference-only, never preferred-pilot.

## 7. Record the review

Before a pilot, add a reviewed commit containing:

- the observation date and refreshed volatile adoption values;
- the upstream version or commit;
- the license and dependency inventory;
- the invocation contract;
- the data-flow and permission review;
- the human approver and approval state.

No install command belongs in this research validation. Installation is a
separate implementation task after the gates pass.
